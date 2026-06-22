-- Better MindScope blog seed data: fewer posts, deeper content.
-- All content is in English.

with
eeg_project as (
  insert into research_projects (
    title,
    slug,
    summary,
    research_question,
    status,
    tags
  )
  values (
    'EEG, Cognition, and Responsible Neurotechnology',
    'eeg-cognition-responsible-neurotechnology',
    'A focused research project on what EEG can measure, what it cannot measure, and how EEG-based claims should be communicated responsibly.',
    'How can EEG-based cognitive research be explained accurately without exaggerating its ability to read thoughts, emotions, or mental states?',
    'active',
    array['eeg', 'neuroscience', 'neurotechnology', 'cognition', 'mindscope']
  )
  on conflict (slug) do update set
    summary = excluded.summary,
    research_question = excluded.research_question,
    status = excluded.status,
    tags = excluded.tags,
    updated_at = now()
  returning id
),
perception_project as (
  insert into research_projects (
    title,
    slug,
    summary,
    research_question,
    status,
    tags
  )
  values (
    'Perception, Prediction, and the Brain',
    'perception-prediction-and-the-brain',
    'A research project about how the brain constructs perception from limited, noisy, and ambiguous sensory information.',
    'How does the brain transform weak or ambiguous sensory signals into conscious perception?',
    'active',
    array['perception', 'vision', 'prediction', 'cognitive-neuroscience', 'mindscope']
  )
  on conflict (slug) do update set
    summary = excluded.summary,
    research_question = excluded.research_question,
    status = excluded.status,
    tags = excluded.tags,
    updated_at = now()
  returning id
),

paper_seed as (
  insert into paper_notes (
    project_id,
    title,
    authors,
    year,
    source_url,
    doi,
    summary,
    methods,
    findings,
    limitations,
    relevance_to_mindscope,
    tags
  )
  values
  (
    (select id from eeg_project),
    'An Introduction to the Event-Related Potential Technique',
    array['Steven J. Luck'],
    2014,
    'https://mitpress.mit.edu/9780262525855/an-introduction-to-the-event-related-potential-technique/',
    null,
    'A major methodological book on how event-related potentials are designed, recorded, processed, and interpreted in cognitive neuroscience.',
    'Textbook-level synthesis of ERP experimental design, EEG recording, preprocessing, averaging, measurement, and interpretation.',
    'ERP research can reveal time-locked neural responses with millisecond-level temporal precision, but valid interpretation depends on careful experimental design and signal processing.',
    'This is a textbook and methodological guide, not a single experimental study.',
    'Core reference for MindScope content explaining EEG, ERP, temporal resolution, experimental design, and why EEG is not direct mind-reading.',
    array['eeg', 'erp', 'methods', 'book', 'cognitive-neuroscience']
  ),
  (
    (select id from eeg_project),
    'Event-related EEG/MEG synchronization and desynchronization: basic principles',
    array['Gert Pfurtscheller', 'F. H. Lopes da Silva'],
    1999,
    'https://pubmed.ncbi.nlm.nih.gov/10576479/',
    '10.1016/S1388-2457(99)00141-8',
    'A foundational review explaining event-related synchronization and desynchronization in EEG and MEG.',
    'Review of oscillatory brain activity and how rhythms change around events, tasks, movement, and cognitive processing.',
    'Brain activity is not only visible as evoked peaks. Ongoing rhythms can increase or decrease in power depending on task demands and neural system engagement.',
    'The principles are general, but exact interpretation depends on task design, frequency band, electrode location, and preprocessing choices.',
    'Useful for MindScope posts about attention, motor imagery, cognitive load, brain rhythms, and responsible interpretation of EEG frequency bands.',
    array['eeg', 'meg', 'oscillations', 'erd', 'ers', 'brain-rhythms']
  ),
  (
    (select id from eeg_project),
    'EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics including independent component analysis',
    array['Arnaud Delorme', 'Scott Makeig'],
    2004,
    'https://pubmed.ncbi.nlm.nih.gov/15102499/',
    '10.1016/j.jneumeth.2003.10.009',
    'A widely cited paper introducing EEGLAB, an open-source environment for EEG analysis.',
    'Software and methods paper describing tools for importing, visualizing, preprocessing, and analyzing EEG data, including independent component analysis.',
    'EEG interpretation requires preprocessing because raw EEG contains artifacts from blinks, muscles, movement, electrodes, and environmental noise.',
    'A toolbox does not make analysis automatically valid; researchers still need appropriate preprocessing decisions and experimental controls.',
    'Useful for MindScope technical posts about EEG cleaning, artifacts, ICA, reproducible workflows, and why raw EEG should not be overinterpreted.',
    array['eeg', 'eeglab', 'ica', 'signal-processing', 'artifacts']
  ),
  (
    (select id from perception_project),
    'Energy, Quanta, and Vision',
    array['Selig Hecht', 'Simon Shlaer', 'Maurice Henri Pirenne'],
    1942,
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC2142545/',
    '10.1085/jgp.25.6.819',
    'A classic psychophysics paper investigating the minimum light energy needed for human visual detection.',
    'Dark-adapted visual threshold experiments measuring the probability of detecting very weak flashes of light.',
    'Human vision can respond to extremely small amounts of light under ideal laboratory conditions, showing how sensitive biological perception can be.',
    'The findings describe controlled threshold detection, not ordinary everyday vision or perfect single-photon awareness.',
    'Useful for MindScope posts about perception, sensory thresholds, rods, uncertainty, and the difference between physical signals and conscious experience.',
    array['vision', 'photons', 'psychophysics', 'perception', 'rods']
  ),
  (
    (select id from perception_project),
    'Why can''t you tickle yourself?',
    array['Sarah-Jayne Blakemore', 'Daniel Wolpert', 'Chris Frith'],
    2000,
    'https://pubmed.ncbi.nlm.nih.gov/10943682/',
    '10.1097/00001756-200008030-00002',
    'A paper discussing why self-generated touch is perceived as less ticklish than externally generated touch.',
    'Review and experimental interpretation based on sensory prediction, motor control, and internal forward models.',
    'The brain predicts the sensory consequences of its own actions, which can attenuate expected self-generated sensations.',
    'Tickling is a specific case; the broader concept of prediction should be applied carefully.',
    'Useful for MindScope posts about prediction, body awareness, sensory filtering, cerebellum, and active perception.',
    array['prediction', 'touch', 'cerebellum', 'sensory-attenuation', 'perception']
  )
  on conflict do nothing
)

insert into blog_posts (
  project_id,
  title,
  slug,
  excerpt,
  author_id,
  content_markdown,
  status,
  tags
)
values
(
  (select id from eeg_project),
  'What EEG Can and Cannot Tell Us About the Brain',
  'what-eeg-can-and-cannot-tell-us-about-the-brain',
  'EEG is powerful because it measures brain activity with millisecond precision, but it cannot directly read thoughts, emotions, or private mental content.',
  'abf4df92-ba3a-46d1-848f-b580e984298c',
$md$
# What EEG Can and Cannot Tell Us About the Brain

Electroencephalography, better known as EEG, is one of the most widely used non-invasive methods for studying human brain activity. It is often shown as a set of electrodes placed on the scalp, producing wave-like traces that seem to reveal the activity of the mind in real time. This image is partly true, but also easy to misunderstand.

EEG does not read thoughts directly. It does not show a mental image, a sentence, a memory, or a private intention. What EEG records are tiny voltage differences measured at the scalp. These voltage changes are related to the coordinated electrical activity of large populations of neurons, especially cortical pyramidal cells. In other words, EEG is a biological signal that reflects patterns of neural activity, not a direct translation of mental content.

## Why EEG is scientifically valuable

The main strength of EEG is temporal resolution. Brain processes can happen very quickly, often within tens or hundreds of milliseconds. EEG is useful because it can track changes at this timescale. This makes it valuable for studying perception, attention, decision-making, language processing, error detection, motor preparation, sleep, and brain-computer interface research.

For example, event-related potential research uses repeated trials to extract neural responses that are time-locked to specific events. If a participant sees a stimulus, hears a sound, makes a decision, or detects an error, researchers can average EEG activity across many similar trials and identify consistent patterns. This approach is central to ERP research.

EEG can also be used to study oscillatory activity. Instead of focusing only on time-locked peaks, researchers can examine changes in frequency bands such as alpha, beta, theta, or gamma. Event-related desynchronization and synchronization describe how ongoing rhythms decrease or increase around a task or event.

## What EEG cannot do

EEG has important limitations. The signal must pass through brain tissue, cerebrospinal fluid, skull, and skin before reaching the electrodes. By the time it reaches the scalp, the signal is spatially blurred. This means EEG is very good at timing but much weaker at precise localization compared with methods such as fMRI or intracranial recordings.

Another limitation is that EEG is sensitive to artifacts. Eye blinks, eye movements, facial muscles, jaw tension, head movement, electrode problems, and environmental electrical noise can all affect the signal. This is why preprocessing is not optional. Raw EEG should not be treated as clean evidence of a cognitive state.

Most importantly, EEG should not be marketed as mind-reading. A system may classify task-related patterns under controlled conditions, but that is different from knowing what a person is thinking. Responsible neurotechnology should describe measurable signals and statistical inferences, not exaggerated claims.

## Why this matters for MindScope

For MindScope, EEG should be presented as a research signal: powerful, fascinating, but limited. A good EEG-based platform should explain what was measured, under what conditions, how the signal was processed, and how confident the interpretation is.

The most scientifically honest message is this: EEG can help us study brain dynamics, attention, perception, sleep, and task-related activity, but it does not provide direct access to thoughts.

## References

- Steven J. Luck, *An Introduction to the Event-Related Potential Technique*, MIT Press, 2014.
- Gert Pfurtscheller and F. H. Lopes da Silva, “Event-related EEG/MEG synchronization and desynchronization: basic principles,” *Clinical Neurophysiology*, 1999. DOI: 10.1016/S1388-2457(99)00141-8.
- Arnaud Delorme and Scott Makeig, “EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics including independent component analysis,” *Journal of Neuroscience Methods*, 2004. DOI: 10.1016/j.jneumeth.2003.10.009.
$md$,
  'draft',
  array['eeg', 'brain-signals', 'neurotechnology', 'mindscope', 'research']
),
(
  (select id from eeg_project),
  'Why Raw EEG Data Is Not Enough',
  'why-raw-eeg-data-is-not-enough',
  'Raw EEG contains brain activity, but it also contains noise from the eyes, muscles, movement, electrodes, and the environment.',
  'abf4df92-ba3a-46d1-848f-b580e984298c',
$md$
# Why Raw EEG Data Is Not Enough

A raw EEG recording can look impressive: dozens of channels changing every millisecond, with complex waves that appear to represent the living brain in action. But raw EEG is not the same thing as meaningful brain data. It is a mixture of neural activity, biological noise, technical artifacts, and environmental interference.

This is one of the most important facts in EEG research. Before an EEG signal can be interpreted, it usually needs to be cleaned, segmented, checked, and analyzed with methods that match the research question.

## What contaminates EEG?

EEG electrodes are placed on the scalp, but the scalp does not only receive signals from the brain. It also picks up activity from many other sources.

Eye blinks can produce large voltage changes. Eye movements can affect frontal electrodes. Muscle activity from the jaw, forehead, neck, or face can introduce high-frequency noise. Movement can disturb electrode contact. Poor impedance can make channels unstable. Even nearby electrical equipment can influence the recording.

This means a strong signal does not automatically mean strong brain activity. Sometimes the strongest part of the recording is an artifact.

## Why preprocessing exists

Preprocessing is the set of steps used to make EEG data more interpretable. Depending on the experiment, this may include filtering, bad channel detection, re-referencing, epoching, baseline correction, artifact rejection, and independent component analysis.

Independent component analysis, often used in tools such as EEGLAB, can help separate statistically independent sources in the data. Some components may reflect eye blinks, muscle activity, or other non-neural sources. Removing or correcting these components can improve the quality of later analysis.

However, preprocessing is not magic. Bad preprocessing can remove useful brain activity or preserve misleading artifacts. Every decision should be documented.

## The danger of overinterpretation

A common mistake in neurotechnology is to treat a live EEG trace as if it directly explains what a person feels or thinks. This is scientifically risky. Without a defined task, a baseline, artifact control, and statistical validation, it is very difficult to make strong claims from raw EEG alone.

For example, saying “this person is focused because alpha changed” is too simplistic. Alpha rhythms can relate to attention, inhibition, eyes-closed states, fatigue, and other factors depending on context. Frequency bands are meaningful only when interpreted inside a specific experimental design.

## What a responsible system should show

A responsible EEG platform should make the processing pipeline visible. It should explain whether the signal is raw or processed, whether artifacts were detected, which channels were used, what features were extracted, and how uncertainty was handled.

For MindScope, this is not just a technical detail. It is part of scientific trust. Users should understand that EEG analysis is not a single measurement but a pipeline of decisions.

## Key takeaway

Raw EEG is valuable, but it is not self-explanatory. It becomes scientifically useful only when collected, cleaned, analyzed, and interpreted carefully.

## References

- Arnaud Delorme and Scott Makeig, “EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics including independent component analysis,” *Journal of Neuroscience Methods*, 2004. DOI: 10.1016/j.jneumeth.2003.10.009.
- Steven J. Luck, *An Introduction to the Event-Related Potential Technique*, MIT Press, 2014.
- Gert Pfurtscheller and F. H. Lopes da Silva, “Event-related EEG/MEG synchronization and desynchronization: basic principles,” *Clinical Neurophysiology*, 1999. DOI: 10.1016/S1388-2457(99)00141-8.
$md$,
  'draft',
  array['eeg', 'signal-processing', 'artifacts', 'eeglab', 'data-quality']
),
(
  (select id from perception_project),
  'The Brain Does Not Simply Record Reality',
  'the-brain-does-not-simply-record-reality',
  'Perception is not a passive recording of the outside world. The brain interprets weak, noisy, and incomplete signals.',
  'abf4df92-ba3a-46d1-848f-b580e984298c',
$md$
# The Brain Does Not Simply Record Reality

It is tempting to imagine perception as a camera-like process: light enters the eyes, sound enters the ears, touch reaches the skin, and the brain records the world. But perception is not a passive recording. It is an active biological process that transforms limited and noisy sensory signals into meaningful experience.

Two classic examples show this clearly: the sensitivity of human vision in very low light and the inability to tickle yourself effectively.

## Vision begins with physical energy, but perception is more than physics

Light is made of discrete packets of energy called photons. In a classic 1942 study, Selig Hecht, Simon Shlaer, and Maurice Henri Pirenne investigated how little light is needed for a person to detect a flash under dark-adapted laboratory conditions.

Their work showed that human vision can be extraordinarily sensitive. Under ideal conditions, the visual system can respond to very small amounts of light. This does not mean everyday vision is perfect or that conscious perception is a simple photon counter. Detection depends on the retina, rod photoreceptors, neural noise, thresholds, attention, and decision-making.

The important point is that perception begins with physical signals, but the final experience is constructed by the nervous system.

## Why you cannot tickle yourself

Tickling shows another side of active perception. Most people cannot tickle themselves with the same intensity that another person can. This is not because the skin stops working. The same skin receptors can still be stimulated. The difference is prediction.

When you move your own hand, the brain can predict many of the sensory consequences of that movement. If the sensation matches the prediction, the brain reduces its response. This process is often explained through internal forward models, where the motor system predicts the expected sensory outcome of an action.

Blakemore, Wolpert, and Frith discussed this mechanism in relation to self-produced touch. The key idea is that the brain treats expected self-generated sensations differently from unexpected external sensations.

## Perception is controlled interpretation

Together, these examples show that the brain does not merely receive information. It filters, predicts, compares, and interprets.

In vision, the nervous system must decide whether weak sensory input is real or noise. In touch, it must distinguish between sensations caused by the outside world and sensations caused by the body itself. In both cases, conscious experience is the result of biological processing, not direct access to reality.

## Why this matters for neuroscience communication

This topic is useful for MindScope because it helps explain a broader principle: brain data should not be interpreted naively. Whether we are discussing perception, EEG, attention, or emotion, the nervous system is always context-dependent.

A signal is not automatically a meaning. A measurement is not automatically an explanation. The brain works through patterns, predictions, thresholds, and uncertainty.

## Key takeaway

Perception is not a camera. It is an active process in which the brain turns incomplete signals into usable experience.

## References

- Selig Hecht, Simon Shlaer, and Maurice Henri Pirenne, “Energy, Quanta, and Vision,” *Journal of General Physiology*, 1942. DOI: 10.1085/jgp.25.6.819.
- Sarah-Jayne Blakemore, Daniel Wolpert, and Chris Frith, “Why can’t you tickle yourself?”, *NeuroReport*, 2000. DOI: 10.1097/00001756-200008030-00002.
$md$,
  'draft',
  array['perception', 'vision', 'prediction', 'cognitive-neuroscience', 'mindscope']
)
on conflict (slug) do update set
  project_id = excluded.project_id,
  excerpt = excluded.excerpt,
  content_markdown = excluded.content_markdown,
  status = excluded.status,
  tags = excluded.tags,
  updated_at = now();