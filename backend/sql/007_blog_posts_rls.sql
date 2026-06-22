alter table public.blog_posts enable row level security;

grant select, insert, update, delete on public.blog_posts to authenticated;
grant select on public.blog_posts to anon;

drop policy if exists "Public blog posts are viewable by everyone" on public.blog_posts;
create policy "Public blog posts are viewable by everyone"
on public.blog_posts
for select
to anon, authenticated
using (
  status = 'published'
  and visibility = 'public'
);

drop policy if exists "Research users can view their own blog posts" on public.blog_posts;
create policy "Research users can view their own blog posts"
on public.blog_posts
for select
to authenticated
using (author_id = auth.uid());

drop policy if exists "Research users can insert their own blog posts" on public.blog_posts;
create policy "Research users can insert their own blog posts"
on public.blog_posts
for insert
to authenticated
with check (
  author_id = auth.uid()
  and exists (
    select 1
    from public.profiles p
    where p.id = auth.uid()
      and p.role = 'research'
  )
);

drop policy if exists "Research users can update their own blog posts" on public.blog_posts;
create policy "Research users can update their own blog posts"
on public.blog_posts
for update
to authenticated
using (
  author_id = auth.uid()
  and exists (
    select 1
    from public.profiles p
    where p.id = auth.uid()
      and p.role = 'research'
  )
)
with check (
  author_id = auth.uid()
  and exists (
    select 1
    from public.profiles p
    where p.id = auth.uid()
      and p.role = 'research'
  )
);

drop policy if exists "Research users can delete their own blog posts" on public.blog_posts;
create policy "Research users can delete their own blog posts"
on public.blog_posts
for delete
to authenticated
using (
  author_id = auth.uid()
  and exists (
    select 1
    from public.profiles p
    where p.id = auth.uid()
      and p.role = 'research'
  )
);
