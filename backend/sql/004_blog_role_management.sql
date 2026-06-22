do $$ begin
  create type blog_visibility as enum ('public', 'private');
exception when duplicate_object then null;
end $$;

alter table if exists public.blog_posts
  add column if not exists author_id uuid;

alter table if exists public.blog_posts
  add column if not exists visibility blog_visibility not null default 'public';

alter table if exists public.blog_posts
  add column if not exists published_at timestamptz;

update public.blog_posts
set published_at = created_at
where status = 'published' and published_at is null;

do $$ begin
  alter table public.blog_posts
    add constraint blog_posts_author_id_fkey
    foreign key (author_id) references public.profiles(id) on delete cascade;
exception
  when duplicate_object then null;
end $$;

update public.blog_posts bp
set author_id = p.id
from public.profiles p
where bp.author_id is null
  and p.id = (
    select pr.id
    from public.profiles pr
    order by
      case when pr.role = 'research' then 0 else 1 end,
      pr.created_at asc
    limit 1
  );

alter table if exists public.blog_posts
  alter column author_id set not null;

create index if not exists idx_blog_posts_author_id on public.blog_posts(author_id);
create index if not exists idx_blog_posts_public_listing on public.blog_posts(status, visibility, published_at desc);
