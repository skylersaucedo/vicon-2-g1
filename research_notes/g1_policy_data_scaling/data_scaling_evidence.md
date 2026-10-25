# Data quantity versus policy performance: humanoid motion tracking, humanoid manipulation, and robot imitation learning (2023 to October 2026)

Scope note. All arXiv identifiers below were checked against the live abstract or HTML page (or the local PDF in `manuscripts/`) during this research pass. "Sim" marks simulation results; "HW" marks real-robot results. "Tracking success" means the robot survives and follows the reference without a termination condition (typically a pelvis or key-body deviation threshold). "Task success" means an object or scene reaches the goal state. Numbers read from figure legends via PDF text extraction are flagged as such. No em-dashes or dollar signs are used in this file.

## Key question 1: Which humanoid motion-tracking papers ran data-quantity ablations, and what curves did they report?

### Takeaway
Only three humanoid tracking papers report performance against the amount of training motion data on a shared evaluation set: ExBody2 (50 vs 250 vs 1,919 CMU clips), SONIC (4M to 100M frames, 20k to 317k clips, three model sizes, three compute budgets) and Humanoid-GPT (2M to 2B frames). None fits a power law. The consistent pattern is that tracking success climbs steeply up to the tens-of-millions-of-frames scale and then flattens (SONIC 98.0 to 99.6 percent tracking success; Humanoid-GPT 83.3 to 92.6 percent), while ExBody2 and OmniClone show that composition and feasibility filtering of the data move the metrics more than raw clip count does. GMT, BeyondMimic, TWIST, Any2Track, HuMBLE, ZEST and Beyond Retargeting report no data-quantity ablation at all.

### Cited Findings

Data points of the form (data quantity, tracking metric):

| Paper | Robot | Setting | Data quantity | Metric | Source |
|---|---|---|---|---|---|
| SONIC | Unitree G1 (29 DoF) | Sim, test-content split | 1.2M-param model, full data | 98.0 percent tracking success, 27.7 mm MPJPE-L | [Sec. 2.1, Fig. 2A to C](https://arxiv.org/abs/2511.07820) |
| SONIC | Unitree G1 | Sim, test-content | 42M-param model, full data (317,189 clips, 611 h, over 100M frames at 50 Hz) | 99.6 percent tracking success, 23.8 mm MPJPE-L | [Sec. 2.1, Table 2, Fig. 2A to C](https://arxiv.org/abs/2511.07820) |
| SONIC | Unitree G1 | Sim, data axis | 4M, 10M, 22M, 100M frames (20k, 50k, 110k, 317k clips) | success improves monotonically along the axis; per-point values only in Fig. 2A to C, not in text; all three axes significant by Welch t-test, P at most 0.011 | [Fig. 2 caption](https://arxiv.org/abs/2511.07820) |
| SONIC | Unitree G1 | Sim, compute axis | 16, 32, 128 GPUs (about 2k, 9k, 21k GPU-hours), 50k iterations each | more GPUs give better asymptotic performance; values in Fig. 2 only | [Sec. 2.1, Fig. 2A to C](https://arxiv.org/abs/2511.07820) |
| SONIC | Unitree G1 | HW, 124 motions | 42M model | 123 of 124 succeed (99.2 percent), 25.7 mm MPJPE-L; sim on the same 124 motions 124 of 124, 22.3 mm | [Sec. 2.1, Fig. 2K to L](https://arxiv.org/abs/2511.07820) |
| Humanoid-GPT | Unitree G1 (29 DoF) | Sim, AMASS test split | MLP (3-layer, 0.25M params), 2M tokens | 76.89 percent SR, MPKPE 100.49 mm, MPJPE 0.1191 rad | [Table 2](https://arxiv.org/abs/2606.03985) |
| Humanoid-GPT | Unitree G1 | Sim | TCN (8-layer, 0.65M), 2M tokens | 81.48 percent SR, MPKPE 79.75 mm | [Table 2](https://arxiv.org/abs/2606.03985) |
| Humanoid-GPT | Unitree G1 | Sim | Humanoid-GPT-S (5.7M), 2M tokens | 83.26 percent SR, MPKPE 62.65 mm | [Table 2](https://arxiv.org/abs/2606.03985) |
| Humanoid-GPT | Unitree G1 | Sim | Humanoid-GPT-S (5.7M), 20M tokens | 86.02 percent SR, MPKPE 46.49 mm | [Table 2](https://arxiv.org/abs/2606.03985) |
| Humanoid-GPT | Unitree G1 | Sim | Humanoid-GPT-B (22.1M), 200M tokens | 88.27 percent SR, MPKPE 44.78 mm | [Table 2](https://arxiv.org/abs/2606.03985) |
| Humanoid-GPT | Unitree G1 | Sim | Humanoid-GPT-B (22.1M), 2B tokens | 90.43 percent SR, MPKPE 41.49 mm | [Table 2](https://arxiv.org/abs/2606.03985) |
| Humanoid-GPT | Unitree G1 | Sim | Humanoid-GPT-L (80.4M), 2B tokens | 92.58 percent SR, MPKPE 40.99 mm, MPJPE 0.0735 rad | [Table 2](https://arxiv.org/abs/2606.03985) |
| Humanoid-GPT | Unitree G1 | Sim, Sec. 5.3 text | MLP-L 75.25 percent SR vs MLP-S 76.89 percent at 2M tokens; TCN-L 79.85 percent vs TCN-S 81.48 percent at 2M tokens; TCN-L 89.05 percent at 2B tokens | larger MLP and TCN underperform smaller ones at 2M tokens; these text numbers do not appear as rows of Table 2 | [Sec. 5.3](https://arxiv.org/abs/2606.03985) |
| ExBody2 | Unitree G1 | Sim, eval on D50 (50 clips) | train on D50 / D250 / full CMU (1,919 clips) | Evel 0.1375 / 0.1454 / 0.1543 m/s; MPKPE 0.0627 / 0.0669 / 0.0767 m; MPJPE 0.0753 / 0.0870 / 0.1099 rad | [Appendix C, Table X(a)](https://arxiv.org/abs/2412.13196) |
| ExBody2 | Unitree G1 | Sim, eval on full CMU | train on D50 / D250 / full CMU | Evel 0.3509 / 0.2834 / 0.2622; MPKPE 0.1076 / 0.1048 / 0.1071; MPJPE 0.1338 / 0.1148 / 0.1291 | [Table X(b)](https://arxiv.org/abs/2412.13196) |
| ExBody2 | Unitree G1 | Sim, eval on ACCAD (OOD) | train on D50 / D250 / full CMU | Evel 0.4226 / 0.3533 / 0.3452; MPKPE 0.1277 / 0.1234 / 0.1267; MPJPE 0.1720 / 0.1421 / 0.1780 | [Table X(c)](https://arxiv.org/abs/2412.13196) |
| ExBody2 | Unitree G1 | Sim and HW, feasibility filter | unfiltered vs filtered CMU | Sim (Table II): MPJPE 0.1355 vs 0.1079, MPKPE 0.1133 vs 0.1000, Evel 0.2787 vs 0.2930; HW (Table III): MPJPE 0.1361 vs 0.1074 | [Tables II and III](https://arxiv.org/abs/2412.13196) |
| SMASH | Unitree G1 | Sim, task tracking score S_R | 64 / 200 / 400 mocap clips (each a 1.08 s strike segment) | 73.61 plus or minus 0.60 / 76.86 plus or minus 0.14 / 76.55 plus or minus 0.19 | [Table IV](https://arxiv.org/abs/2604.01158) |
| SMASH | Unitree G1 | Sim | 400 clips plus 2k / 5k / 10k generated strikes | 82.32 / 86.38 / 85.88; 60 clips plus 5k generated 83.06; 200 clips plus 5k generated 85.29 | [Table IV](https://arxiv.org/abs/2604.01158) |
| SMASH | Unitree G1 | HW | 400-5k-gen policy | mocap perception 20 of 20 hits, 18 of 20 returns; ego-camera 19 of 20 hits, 12 of 20 returns; 642 launches over 50 min, 93.7 percent contact, 59.7 percent return | [Sec. VI-B, Table V](https://arxiv.org/abs/2604.01158) |
| SCHUR | Unitree G1 (29 DoF) | Sim, tokenizer | 20 percent of a 260 h, 170k-sequence corpus vs full | tokenizer MPJPE 0.0483 vs 0.0326, MPKPE 0.0497 vs 0.0372 (Table I); generation FID 23.5 vs 12.6, R at 1 0.653 vs 0.719 (Table II) | [Tables I and II](https://arxiv.org/abs/2511.09241) |
| SCHUR | Unitree G1 | Sim, tracker | raw robot data / human-motion retarget / filtered (Ours) | tracking success 0.762 / 0.774 / 0.907 (full-dataset reference 0.911); MPJPE 0.1095 / 0.1183 / 0.0893 | [Table III](https://arxiv.org/abs/2511.09241) |
| OmniClone | Unitree G1 (29 DoF plus Inspire hands) | Sim (MuJoCo, OmniBench) | 30 h AMASS plus LAFAN; recipe variants Dynamic, Stable, Balance, final filtered | Dynamic variant SR collapses to 10 to 30 percent on loco-manipulation categories while the final recipe holds 100 percent; MPJPE 36 to 48 mm for the final recipe vs 128 to 180 mm for GMT on loco-manipulation (values read from layout-extracted Table I, column alignment uncertain) | [Table I, Fig. 4, Sec. V](https://arxiv.org/abs/2603.14327) |

Qualitative and framing findings:

- SONIC trained on 317,189 clips, 611 h, over 100 million frames at 50 Hz, after filtering physically implausible motions from about 700 source hours; the paper fits no power law and reports no exponent, and the authors frame the result as "scaling data, model size and compute" with the largest gains on out-of-distribution motions. [SONIC, Table 2 and Sec. 2.1](https://arxiv.org/abs/2511.07820)
- SONIC supplementary Sec. S2.5 reports that a specialist locomotion controller (OpenHomie) saturated at 8 GPUs (0.18 m/s tracking error, 95.0 percent survival) and did not improve at 32 GPUs (0.29 m/s, 91.2 percent), while the motion tracker "continued to benefit from additional capacity and data throughput". [SONIC, Sec. S2.5, Fig. S6](https://arxiv.org/abs/2511.07820)
- SONIC vs other trackers in simulation (not data-matched): SONIC 98.5 / 99.2 / 97.2 percent success on test-content / test-repetition / PHUMA; BeyondMimic 82.0 / 85.4 / 73.8; Any2Track 61.6 / 69.4 / 78.5; MPJPE-L 23.7 mm vs 40.9 mm for BeyondMimic. [SONIC, Fig. 2D to G](https://arxiv.org/abs/2511.07820)
- Humanoid-GPT trains on about 2B G1-retargeted frames from AMASS, LAFAN1, MotionMillion and PHUMA (plus Motion-X++ and internal mocap per the introduction), "over 200 times" larger than prior tracker training sets; time-warp augmentation expands the data about 5 times; about 384 PPO experts and about 15,000 GPU-hours. The text says marginal gains shrink between 200M and 2B tokens, which the authors read as the onset of a data-limited regime. The introduction says the authors "derive a scaling law" but no fitted equation or exponent appears in the paper. [Humanoid-GPT, Sec. 3.1, Sec. 6, Table 8](https://arxiv.org/abs/2606.03985)
- Humanoid-GPT hardware: MPJPE / MPJVE on four unseen dance clips for Humanoid-GPT-B: 0.0974 / 0.9813, 0.1075 / 1.2257, 0.0858 / 0.6158, 0.0856 / 0.7325; no hardware success rate is reported. [Humanoid-GPT, Table 3](https://arxiv.org/abs/2606.03985)
- ExBody2 trains on 1,919 CMU sequences; the authors state "additional data does not necessarily benefit in-distribution tasks" and that the 250-clip subset "generalizes better than the one trained on DCMU", attributing the drop to "noisy datasets" containing infeasible motions; they call this the Feasibility-Diversity Principle. [ExBody2, Appendix C, Table X](https://arxiv.org/abs/2412.13196)
- GMT trains on a curated 8,925-clip, 33.12 h subset of AMASS and LAFAN1 on a 23-DoF G1; no data-quantity ablation; its ablation is adaptive sampling and MoE: AMASS MPKPE 42.07 mm (full) vs 43.54 (no adaptive sampling) vs 44.34 (no AS and no MoE); no success rate reported. [GMT, Table 1 and Table 2a](https://arxiv.org/abs/2506.14770)
- BeyondMimic trains on about 2.5 h of human motion and deploys 30 clips (about 15 min) on hardware; no data-quantity ablation; adaptive sampling halves iterations for one motion (2k vs 4k) and without it three of four motions fail segments after 30k iterations. [BeyondMimic, Results and Fig. 8B](https://arxiv.org/abs/2508.08241)
- TWIST trains on over 15,000 AMASS and OMOMO clips (about 42 h) plus 150 in-house clips (about 0.5 h); Key Finding 2 is that adding the small in-house set, retargeted online, "substantially reduces tracking errors on unseen motions" (Fig. 6 left, Fig. 7 right); numbers appear only in plots and no dataset-size sweep is reported. [TWIST, Sec. 3.1 and Sec. 4.2](https://arxiv.org/abs/2505.02833)
- Any2Track ("Track Any Motions under Any Disturbances") reports 18.34 mm MPJPE under disturbances on the G1 vs 37.21 mm for a PPO baseline; the abstract page shows no data-quantity ablation. [Any2Track, abstract](https://arxiv.org/abs/2509.13833)
- Beyond Retargeting trains on 14,147 training and 4,073 testing clips from AMASS, LAFAN1 and OMOMO and evaluates on 6,495 SONIC bones-seed trajectories; its codebook-capacity sweep over an 8 times range leaves SR in 0.932 to 0.943, so capacity rather than data is swept. [Beyond Retargeting, Sec. IV, Table V](https://arxiv.org/abs/2610.07891)
- HuMBLE trains on an in-house locomotion dataset of 528,214 frames (about 3 h) and explicitly defers "a rigorous scalability analysis" to future work. [HuMBLE, Discussion](https://arxiv.org/abs/2610.10489)
- ZEST reports per-skill tracking on Atlas, G1 and Spot and simulation ablations on curriculum and adaptive sampling (success after 10 h and 20 h of training); no data-quantity ablation. [ZEST, Fig. 2e to f](https://arxiv.org/abs/2602.00401)
- OmniClone: "the composition of even a small fraction of the training data can decisively steer policy behavior"; standing manipulation is about 60 percent of the 30 h dataset, and subtle changes to the dynamic/locomotion fraction plus filtering of biased sequences steer the policy. Training cost about 80 GPU-hours on one RTX 4090. [OmniClone, Sec. V-A, Sec. VII](https://arxiv.org/abs/2603.14327)

### Inferences
- Across SONIC and Humanoid-GPT, tracking success in simulation moves from roughly 77 to 83 percent at 2M frames to 90 to 93 percent at 2B frames (Humanoid-GPT) and from 98.0 to 99.6 percent across model size at about 100M frames (SONIC). The last few percentage points cost two to three orders of magnitude more data, which is a saturating curve, not a power law anyone has fit. Inference, not a reported claim.
- The ExBody2 and SCHUR results indicate that for RL tracking policies, the count of clips is a weaker lever than the fraction of physically feasible clips: a 250-clip filtered set beat a 1,919-clip raw set on out-of-distribution ACCAD MPJPE by 20 percent (0.1421 vs 0.1780 rad). Inference from Table X values.
- For a Vicon-to-G1 pipeline, the relevant regime is tens of minutes to a few hours of task-specific motion, which is far below where any tracking paper ran an ablation; the SMASH 64-vs-400-clip result (73.6 vs 76.6 score) and the TWIST 0.5 h in-house addition are the closest evidence that a small, well-targeted mocap set measurably changes a tracker trained on a large public base. Inference.

### Gaps
- SONIC's per-point success and MPJPE for 4M, 10M, 22M and 100M frames are only in Fig. 2A to C as plotted curves; the text and supplement do not tabulate them.
- Humanoid-GPT's Fig. 6 data-scaling curve values are not in the text; Sec. 5.3 numbers conflict with Table 2 (see table note).
- No humanoid tracking paper reports hardware success rate as a function of training-data quantity. All data-quantity curves are simulation.
- OmniClone Table I values were read from a layout-extracted PDF; column alignment for the ablation variants is uncertain and should be checked against the PDF before quoting individual cells.
- HumanoidVerse is a training framework, not a paper with a data ablation; nothing to report.
- SMASH's S_R metric is not defined as a percentage in the extracted text; treat it as a task-tracking score.

## Key question 2: Which humanoid manipulation or VLA papers report success rate as a function of number of demonstrations on the G1 or similar humanoids?

### Takeaway
Hardware demonstration-count sweeps on humanoids are sparse. The cleanest are GR00T N1 (GR-1 humanoid, 10 percent vs full data, 42.6 vs 76.8 percent), OmniH2O (Unitree H1, 25/50/100 percent of 40 min of teleop data gives 4/10, 6.5/10, 8/10), HumanoidExo (G1, 5 teleop demos 5 percent vs 5 plus 195 exoskeleton demos about 80 percent vs 200 teleop demos 80 percent), lambda-0 (G1, Stage-II human-data fraction 0 to 100 percent raises task progress 59.9 to 80.4 percent), and OmniClone (G1, 50 demos gives 85.71 and 80.00 percent). GR00T N1.5 on the G1 reaches 98.8 percent with 1,000 teleop episodes. In simulation, GR00T N1 on the GR-1 benchmark goes 43.2 to 50.0 to 49.3 percent at 30, 100, 300 demos, which is flat beyond 100.

### Cited Findings

Data points of the form (demonstrations, task success):

| Paper | Robot | HW or Sim | Data quantity | Task success | Source |
|---|---|---|---|---|---|
| GR00T N1 | Fourier GR-1 | HW, average over 4 task categories | 10 percent of teleop data (full data was 15 min to 3 h per task) | GR00T-N1-2B 42.6 percent; Diffusion Policy 10.2 percent | [Table 3](https://arxiv.org/abs/2503.14734) |
| GR00T N1 | GR-1 | HW | full data | GR00T-N1-2B 76.8 percent; Diffusion Policy 46.4 percent | [Table 3](https://arxiv.org/abs/2503.14734) |
| GR00T N1 | GR-1 | HW, per task 10 percent / full | Pick-and-Place seen 36.0 / 92.0; unseen 34.0 / 72.0; White Drawer 26.4 / 79.9; Dark Cabinet 86.6 / 69.7; Wooden Chest 72.9 / 63.2; Machinery Packing 8.0 / 56.0; Mesh Cup Pouring 65.0 / 67.5; Cylinder Handover 20.0 / 86.6; Coordination 1 70.0 / 80.0; Coordination 2 30.0 / 85.0 | percent | [Table 5](https://arxiv.org/abs/2503.14734) |
| GR00T N1 | GR-1 sim benchmark | Sim, 30 / 100 / 300 demos per task | GR00T-N1-2B 43.2 / 50.0 / 49.3; Diffusion Policy 21.3 / 32.7 / 40.4 | percent | [Table 4, Fig. 10](https://arxiv.org/abs/2503.14734) |
| GR00T N1 | RoboCasa (Franka) | Sim, 30 / 100 / 300 | GR00T 17.4 / 32.1 / 49.6; DP 14.7 / 25.6 / 43.2 | percent | [Table 4](https://arxiv.org/abs/2503.14734) |
| GR00T N1 | DexMimicGen bimanual | Sim, 30 / 100 / 300 | GR00T 29.6 / 58.5 / 74.2; DP 23.7 / 46.9 / 68.4 | percent | [Table 4](https://arxiv.org/abs/2503.14734) |
| GR00T N1.5 | RoboCasa | Sim, 30 demos per task | N1 17.4 percent, N1.5 47.5 percent | percent | [NVIDIA GEAR N1.5 page, Table 1](https://research.nvidia.com/labs/gear/gr00t-n1_5/) |
| GR00T N1.5 | Sim GR-1 | Sim, 0-shot / 30 demos | N1 39.6 / 43.2; N1.5 43.9 / 47.4 | percent | [GEAR N1.5 page, Table 1](https://research.nvidia.com/labs/gear/gr00t-n1_5/) |
| GR00T N1.5 | Unitree G1 | HW, 1,000 teleop episodes, place one of two fruits (4 fruits) | N1 44.0 percent, N1.5 98.8 percent; N1.5 on 5 unseen objects 84.2 percent | percent | [GEAR N1.5 page, Table 3](https://research.nvidia.com/labs/gear/gr00t-n1_5/) |
| OmniClone plus GR00T N1.6 | Unitree G1 | HW | 50 full-body demos (whole-body data via OmniClone teleop; 20k post-training steps, batch 384, frozen VLM) | Pick-and-Place 18 of 21 (85.71 percent); Squat to Pick-and-Place 4 of 5 (80.00 percent) | [Table II, Sec. VI-B, Appendix C-B](https://arxiv.org/abs/2603.14327) |
| OmniH2O | Unitree H1 | HW demos; diffusion policy (DP-DDPM) | 25 / 50 / 100 percent of about 40 min teleop data (73,462 frames at 30 Hz across 6 tasks) | average 4/10, 6.5/10, 8/10 (Table 3a); per task Catch-Release 1/10, 3/10, 6/10; Squat 9/10, 10/10, 10/10; Hammer-Catch 3/10, 6/10, 6/10; Rock-Paper-Scissors 3/10, 9/10, 10/10 (Table 17a) | [Tables 3 and 17, Appendix J](https://arxiv.org/abs/2406.08858) |
| HumanoidExo | Unitree G1 (29 DoF plus Inspire hands) | HW | PlaceToy: 5 teleop demos / 5 teleop plus 195 exoskeleton demos | 5 percent / about 80 percent | [Sec. 4.2, Fig. 6](https://arxiv.org/abs/2510.03022) |
| HumanoidExo | Unitree G1 | HW | PlaceLaundry seen cloth: 200 teleop / 5 teleop plus 195 exo / 5 teleop | 80 / 80 / 5 percent; unseen cloth 80 / 75 / 5 percent | [Table 1](https://arxiv.org/abs/2510.03022) |
| HumanoidExo | Unitree G1 | HW | Walk and PlaceToy: 5 stationary teleop plus 195 exo demos with walking | walking segment 100 percent of trials; overall "matches" stationary task, no number | [Sec. 4.3](https://arxiv.org/abs/2510.03022) |
| lambda-0 | Unitree G1 (GoPro head cam, BrainCo Revo2 hands) | HW, task progress | Stage-II human data fraction 0 / 5 / 10 / 25 / 50 / 100 percent of HumanVerse (500 h, 32,993 episodes, 87M frames, 827 task types) | 59.9 / 64.2 / 67.3 / 72.1 / 76.4 / 80.4 percent progress | [Fig. 12, Sec. 5.3](https://arxiv.org/abs/2610.18950) |
| lambda-0 | Unitree G1 | HW, 40 trials | full recipe vs pi0.5 | 62.5 percent success (25 of 40), 80.4 percent progress vs pi0.5 40.0 percent (16 of 40), 54.0 percent | [Table 1](https://arxiv.org/abs/2610.18950) |
| lambda-0 | Unitree G1 | HW, per-task policies on Close Laptop and Pull Curtain | 200 human demos vs 50 robot demos | 53.3 percent vs 60.0 percent mean task score; 33.30 vs 140.85 person-seconds per demo | [Fig. 9, Sec. 5.1](https://arxiv.org/abs/2610.18950) |
| Humanoid Policy tilde Human Policy (PH2D) | Unitree H1 and H1_2 with Inspire hands | HW | about 250 to 400 robot demos per task; ACT robot-only vs HAT co-trained with human data | in-distribution 42/60 (70 percent) vs 49/60 (82 percent); out-of-distribution 59/170 (35 percent) vs 101/170 (59 percent) | [Table 2, Sec. 4](https://arxiv.org/abs/2503.13441) |
| PH2D | Unitree H1_2 | HW, few-shot cross-embodiment | 20 robot demos on Humanoid B | co-trained policy "substantially" beats robot-only; values only in Fig. 5a | [Fig. 5a and 5b](https://arxiv.org/abs/2503.13441) |
| EgoMimic | bimanual ViperX 300 S (not humanoid) | HW, Continuous Object-in-Bowl, task points | 3 h robot data (ACT) vs 2 h robot plus 1 h human (EgoMimic) | 74 vs 128 points; 1 h human data is about 1,400 demos, 1 h robot data about 135 demos | [Sec. IV-B, Fig. 8, Table II](https://arxiv.org/abs/2410.24221) |
| EgoVLA | Unitree H1 plus Inspire hands | Sim only (Isaac Lab) | 50 percent vs 100 percent of 100 demos per task over 12 tasks | short-horizon seen 48.15 vs 77.78 percent; long-horizon seen 7.41 vs 45.93 percent | [Tables 1 and 2](https://arxiv.org/abs/2507.12440) |
| Being-H0 | Franka FR3 plus Inspire hand (not humanoid) | HW, 20 trials per task | 25 / 50 / 100 percent of teleop fine-tuning data | Being-H0 at 25 percent matches InternVL3 baseline at 100 percent on Pick-Place-Toy; Close-Lid baseline 0 percent vs Being-H0 15 percent at 25 percent data; full-data success Being-H0 0.75 / 0.65 / 0.60 / 0.85 / 0.60 / 1.00 / 0.75 across seven settings vs GR00T N1.5 0.75 / 0.40 / 0.50 / 0.80 / 0.50 / 0.90 / 0.60 | [Fig. 12, Table 7](https://arxiv.org/abs/2507.15597) |
| Isaac Lab Mimic (Franka stacking) | Franka | Sim | 10 source human demos to 1,000 generated demos; generation success about 40 percent | BC-RNN policy about 40 to 60 percent over 50 rollouts | [Isaac Lab docs](https://isaac-sim.github.io/IsaacLab/main/source/features/imitation-learning/teleop_imitation.html) |
| Teleopit | humanoid (platform not named on abstract page) | HW | 96 successful demos | ACT 90.0 percent, GR00T N1.7 95.0 percent | [abstract](https://arxiv.org/abs/2608.01834) |
| Humanoid Everyday | Unitree G1 (Dex3-1 hands) and H1 | HW, 10 trials per task, 7 tasks | about 40 episodes per task (10.3k trajectories, 260 tasks) | average DP 29, DP3 34, ACT 34, OpenVLA 39, pi0-FAST 37, pi0.5 36, GR00T N1.5 51 percent | [Table II](https://arxiv.org/abs/2510.08807) |
| ACT sensor ablation | Unitree G1 with three-finger hands | HW, at most 250 demos | minimal active stereo camera setup | 87.5 percent (spatial generalization task), 94.4 percent (structured task); adding pressure sensors drops the latter to 67.3 percent | [abstract](https://arxiv.org/abs/2603.28422) |

Framing statements:

- GR00T N1: "GR00T-N1-2B at 10 percent data is only 3.8 percent lower than Diffusion Policy at full data" (42.6 vs 46.4 percent). Pre-training neural trajectories expanded 88 h of in-house teleop to 827 h of generated video; 780,000 simulated trajectories equal about 6,500 h of demonstrations. [GR00T N1, Sec. on real-world results, Table 3](https://arxiv.org/abs/2503.14734)
- GR00T N1 Table 2 DexMG at 100 demos (DP 56.1, GR00T 66.5) does not match Table 4 at 100 demos (46.9, 58.5); the paper does not explain this. [GR00T N1, Tables 2 and 4](https://arxiv.org/abs/2503.14734)
- GR00T N1.5 page: N1.5 is "significantly better in the very low data regime (0-shot and 30 demos)". [GEAR N1.5 page](https://research.nvidia.com/labs/gear/gr00t-n1_5/)
- GR00T N1.6 page states pretraining on "several thousand hours of teleoperated data" including Unitree G1 whole-body loco-manipulation, with 300K pretraining steps at batch 16,384 and post-training of 10K to 30K steps, but gives no success rates, episode counts or N1.5 comparison numbers. [GEAR N1.6 page](https://research.nvidia.com/labs/gear/gr00t-n1_6/)
- HumanoidExo frames exoskeleton data as "scalable" but tests only 0 vs 195 exo demos; there is no sweep over exo-demo count. [HumanoidExo, Sec. 4.2](https://arxiv.org/abs/2510.03022)
- lambda-0 Stage-II validation loss falls 35.5 percent (representative holdout) and 40.6 percent (clean holdout) from 5 to 100 percent of the data, with log-linear fits of R squared 0.9868 and 0.9901, single run. Removing Stage II drops hardware success from 62.5 to 22.5 percent (Table 3). [lambda-0, Fig. 11, Table 3](https://arxiv.org/abs/2610.18950)
- OmniH2O: 50 percent average in Table 3 (6.5/10) does not equal the mean of Table 17 per-task 50 percent values (7.0/10). [OmniH2O](https://arxiv.org/abs/2406.08858)
- Community reproduction of GR00T N1.6 on the G1 PnPAppleToPlate task reports 5 of 10 (50 percent) closed-loop success and notes difficulty reproducing the published G1 checkpoints. This is a third-party model card, not a paper. [HuggingFace model card](https://huggingface.co/cloudwalk-research/GR00T-N1.6-G1-PnPAppleToPlate)
- A G1 fine-tuning paper reports GR00T N1.5 fine-tuned at 48.0 percent and a contact-state-augmented variant at 94.0 percent on Pick Apple to Bowl with 5K embodiment-aligned demonstrations; not a demo-count sweep. [Modality-Augmented Fine-Tuning, Table I](https://arxiv.org/abs/2512.01358)

### Inferences
- On the GR-1 humanoid simulation benchmark, GR00T N1 saturates between 100 and 300 demos per task (50.0 vs 49.3 percent), while Diffusion Policy from scratch keeps improving (32.7 to 40.4 percent). Pretrained VLAs reach their plateau with fewer demos, but the plateau itself is set by the task and the controller, not the data. Inference from Table 4.
- The humanoid hardware numbers cluster: 50 demos gives 80 to 86 percent on two G1 whole-body pick-and-place tasks (OmniClone), 200 teleop demos or 5 plus 195 exo demos gives 80 percent (HumanoidExo), 1,000 episodes gives 98.8 percent on a simple fruit task (GR00T N1.5). The spread is driven more by task difficulty and base model than by demo count. Inference.
- OmniH2O is the only humanoid study with a per-task 25/50/100 percent sweep on hardware-collected data; easy tasks (Squat) saturate at 25 percent (about 2 to 3 min of data), while contact-rich dynamic tasks (Catch-Release) are still rising at 100 percent (about 5 min). Inference from Table 17.
- No published G1 study varies robot demonstration count across more than two levels on hardware. The report writer should state this explicitly rather than imply a curve exists.

### Gaps
- GR00T N1 Table 7 (per-dataset pretraining hours) was not retrieved.
- PH2D Fig. 5a and 5b values (success vs number of Humanoid B demos) are only in the figure; the text gives no numbers.
- EgoMimic Fig. 8 intermediate points (success vs hours of human or robot data) are only in the figure.
- Being-H0 does not report the absolute number of post-training demos per task.
- GR00T N1.6 official success rates on the G1 and simulation benchmarks were not found on the NVIDIA page or the model card.
- CLONE ([2506.08931](https://arxiv.org/abs/2506.08931)), HOMIE ([2502.13013](https://arxiv.org/abs/2502.13013)) and PhysHSI ([2510.11072](https://arxiv.org/abs/2510.11072)) abstracts report no demonstration-count or success-rate numbers relevant to data scaling; full texts were not read.
- Teleopit does not name its humanoid platform on the abstract page and the 20-trial count seen in a search snippet could not be confirmed.

## Key question 3: What do general robot data-scaling studies say about demonstrations vs success, with fitted exponents and saturation points?

### Takeaway
The only published power-law fits for imitation learning in manipulation are from Lin et al. (ICLR 2025): the optimality gap (1 minus normalized score) falls as a power of the number of training objects (exponent about -0.70), environments (-0.47 to -0.84) and environment-object pairs (-0.58 to -0.68), with Pearson r of 0.94 to 0.99, while demonstrations per environment show only a weak relation (r -0.62 and -0.79) and plateau at about 50 per environment-object pair. RT-1, robomimic, Diffusion Policy benchmarks and pi0.5 agree that diversity (tasks, scenes, locations) matters more than demonstration count once each condition has a modest number of demos, and that simple tasks saturate at 50 to 100 demos while hard tasks keep improving at 200 and beyond.

### Cited Findings

Fitted power laws (Lin et al., Y = optimality gap = 1 minus normalized score, X = count; the PDF legend lost the minus sign of the exponent in text extraction, but the gap decreases with X, so exponents are negative):

| Task | X | Fit | Pearson r | Source |
|---|---|---|---|---|
| Pour Water | training objects | 0.825 times X to the power -0.703 | 0.987 | [Fig. 5](https://arxiv.org/abs/2410.18647) |
| Pour Water | training environments | 1.180 times X to the power -0.844 | 0.960 | [Fig. 5](https://arxiv.org/abs/2410.18647) |
| Pour Water | env-object pairs | 1.068 times X to the power -0.579 | 0.980 | [Fig. 5](https://arxiv.org/abs/2410.18647) |
| Mouse Arrangement | training objects | 0.826 times X to the power -0.697 | 0.991 | [Fig. 5](https://arxiv.org/abs/2410.18647) |
| Mouse Arrangement | training environments | 0.827 times X to the power -0.466 | 0.966 | [Fig. 5](https://arxiv.org/abs/2410.18647) |
| Mouse Arrangement | env-object pairs | 1.263 times X to the power -0.683 | 0.942 | [Fig. 5](https://arxiv.org/abs/2410.18647) |
| Pour Water (MSE) | objects / envs / pairs | 0.007 X^-0.080 (r 0.558) / 0.013 X^-0.288 (r 0.951) / 0.017 X^-0.317 (r 0.948) | | [Fig. 20, Appendix G.1](https://arxiv.org/abs/2410.18647) |
| Mouse Arrangement (MSE) | objects / envs / pairs | 0.004 X^-0.250 (r 0.951) / 0.004 X^-0.265 (r 0.952) / 0.005 X^-0.317 (r 0.958) | | [Fig. 20](https://arxiv.org/abs/2410.18647) |

Lin et al. further findings:

- Fits use 6 data points (1, 2, 4, 8, 16, 32) with 100 percent of demonstrations; the authors judge a three-parameter fit with an irreducible-error term "not statistically justified" with 6 points. [Sec. 4.2, footnote 1](https://arxiv.org/abs/2410.18647)
- "When the number of environments and objects is fixed, there is no clear power-law relationship between the number of demonstrations and the policy's generalization performance"; correlation coefficients for total demonstrations are -0.62 (Pour Water) and -0.79 (Mouse Arrangement). [Sec. 4.2, Fig. 7 caption](https://arxiv.org/abs/2410.18647)
- With 16 environments times 64 objects (over 6,400 demos collected), performance plateaus at 800 total demonstrations (8 policies trained from 64 to 6,400 demos). With M = N environment-object pairs, performance plateaus at 400, 800 and 1,600 total demos for 8, 16 and 32 pairs. Recommendation: "collecting 50 demonstrations per environment-object pair (K = 50) for tasks of similar difficulty to ours. More challenging dexterous manipulation tasks may require more demonstrations." [Sec. 4.3, Fig. 7](https://arxiv.org/abs/2410.18647)
- Appendix: "Once the total reaches around 16 times (approximately 1,600 demonstrations), further increases offer minimal performance improvements", even when controlling for total demos, more environments or objects still helps (Fig. 23). [Appendix](https://arxiv.org/abs/2410.18647)
- 8 objects give normalized score above 0.8, 32 objects above 0.9 (object generalization, Fig. 2). Environment-scaling curves for 50 percent and 100 percent of demos overlap (Fig. 3); env-object curves for 25 percent and 100 percent overlap (Fig. 4). [Sec. 4.1](https://arxiv.org/abs/2410.18647)
- Extrapolation: reaching 0.99 normalized score on Mouse Arrangement in new environments with new objects would need 1,191 environment-object pairs (unverified). [Sec. 4.2](https://arxiv.org/abs/2410.18647)
- Verification tasks: 32 env-object pairs times 50 demos (about 1,600 demos per task) collected in one afternoon by four collectors; success in 8 unseen environments with unseen objects (5 trials each): Pour Water 85.0 plus or minus 19.4, Mouse Arrangement 92.5 plus or minus 9.7, Fold Towels 87.5 plus or minus 17.1, Unplug Charger 90.0 plus or minus 14.1 percent; normalized scores 0.922, 0.933, 0.95, 0.887. Over 40,000 demonstrations and 15,000 real rollouts in total; UMI handheld gripper, Diffusion Policy. [Table 1, Sec. 5](https://arxiv.org/abs/2410.18647)
- Multiple objects per environment help only when environments are few; beyond about 16 environments the gain is negligible, so one object per environment is recommended. [Sec. 4.3, Fig. 6](https://arxiv.org/abs/2410.18647)

Other general studies:

- RT-1 (130k episodes, 744 instructions, 13 robots, 17 months). Table 7 data ablations, success percent for Seen / All / Unseen / Distractors / Backgrounds: full 97 / 73 / 76 / 83 / 59; capped at 200 per task (51 percent of data) 71 / 50 / 52 / 39 / 59; capped at 100 per task (37 percent) 55 / 46 / 57 / 35 / 47; capped at 50 per task (22 percent) 59 / 29 / 14 / 31 / 41; 75 percent of tasks with 97 percent of data 86 / 54 / 67 / 42 / 53. Conclusion: removing 25 percent of tasks hurt generalization as much as removing 49 percent of data; "data diversity is more essential than data quantity". [RT-1, Table 7, Sec. 6.5](https://arxiv.org/abs/2212.06817)
- robomimic (200 proficient-human demos per task): BC-RNN at 100 percent data gives Lift 100.0, Can 100.0, Square 84.0, Transport 71.3 plus or minus 6.6, Tool Hang 19.3 plus or minus 5.0 percent (Table 1). Lift and Can "can yield proficient policies (75 to 100 percent success rate) using a small fraction of the data (20 percent)"; for harder tasks "moving from 20 percent to 50 percent or 50 percent to 100 percent size can result in significant policy improvement". 300-demo Multi-Human datasets scored below 200-demo Proficient-Human datasets. Per-fraction tables are in Appendix L (Tables 27 and 28), not retrieved. [robomimic](https://arxiv.org/abs/2108.03298)
- Diffusion Policy on robomimic image tasks as a function of demos (Waypoint-Based Imitation Learning, Table 2; average of max over 3 seeds, 30 initial conditions): Lift 100 / 100 / 100 / 100 at 30 / 50 / 100 / 200 demos; Can 61.0 / 82.3 / 93.3 / 97.3; Square 44.3 / 57.3 / 82.0 / 95.0 percent. [Table 2](https://arxiv.org/abs/2307.14326)
- OpenVLA fine-tuning: 10 to 150 demos per target task on Franka-Tabletop and Franka-DROID; 129 rollouts per method; "OpenVLA is the only approach that achieves at least 50 percent success rate across all tested tasks"; Diffusion Policy from scratch is competitive on narrow single-instruction tasks; pretraining on 970k Open X-Embodiment trajectories. Per-task numbers are in Table 7 (not retrieved) and Fig. 5. [OpenVLA, Sec. 5.2](https://arxiv.org/abs/2406.09246)
- pi0: pretraining on over 10,000 h of robot data; fine-tuning uses "only 5 hours" for the simplest tasks and "100 or more hours" for the most complex; a 1 h Tupperware-in-microwave policy is "significantly better" with pretraining than baselines and pretraining gives up to 2 times improvement over scratch; full model "attains more than 50 percent of the maximum score across all of the tasks" (Fig. 13). Exact per-hour success values are in Fig. 11 only. [pi0, Sec. V-A, Fig. 11, Fig. 13](https://arxiv.org/abs/2410.24164)
- pi0.5: about 400 h of mobile-manipulation data from about 100 homes; models trained on 3, 12, 22, 53, 82 and 104 locations improve with locations on four unseen-home tasks (Fig. 8, values only in figure); a control trained directly on test-home data "attains similar performance as the final 104-location model". [pi0.5, Fig. 8](https://arxiv.org/abs/2504.16054)
- Guiding Data Collection via Factored Scaling Curves (Franka, sim and real): success vs demos per factor fitted as 1 minus a times (n plus base)^b with b less than 0; "as few as four values of n are often sufficient" to fit; no exponents published; FSC allocation gives 54.9 percent at budget K = 20 and 66.9 percent at K = 100 vs 48.1 and 55.4 percent for equal allocation (Table 1, sim average of five tasks). [Sec. on method, Table 1](https://arxiv.org/abs/2505.07728)
- Scaling Single Human Demonstrations (Franka, SAPIEN sim, 5 meshes): 200 / 600 / 800 generated demos; 600 to 800 improves average success by 1.1 percent; 3 to 5 meshes at 800 demos improves by 5.2 percent (Fig. 3, per-point values only in figure); sim mean 37.5 plus or minus 3.0 percent, real 21 to 64 percent. [Table I, Fig. 3, Sec. IV-D](https://arxiv.org/abs/2602.12734)
- LingBot-VLA (dual-arm, 9 embodiments): pretraining scaled from 3,000 to 20,000 h on 25 tasks shows "a consistent upward trend" in progress and success with "no signs of saturation even at the 20,000-hour mark" (Fig. 5, values only in figure); post-training with 80 demos per task on Agibot G1 outperforms pi0.5 with the full 130-demo set (Fig. 6). [Sec. on scaling, Figs. 5 and 6](https://arxiv.org/abs/2601.18692)
- SCHUR (G1, high-level motion generation): 20 percent of a 260 h corpus degrades tokenizer MPJPE from 0.0326 to 0.0483 and generation FID from 12.6 to 23.5. [Tables I and II](https://arxiv.org/abs/2511.09241)

### Inferences
- The Lin et al. environment and object exponents (magnitude 0.47 to 0.84) are steeper than language-model data exponents, and the authors warn that with 6 points and no irreducible term the fits are predictive only within about one order of magnitude. Inference.
- Combining Lin et al. (50 demos per env-object pair, plateau at about 800 to 1,600 total), robomimic (20 percent of 200 is enough for easy tasks), and Waypoint Table 2 (Can 82 percent at 50, Square 82 percent at 100), a single-scene manipulation policy with Diffusion Policy or ACT typically crosses 80 percent at 50 to 100 demos for pick-and-place-grade tasks and at 100 to 200 for precision insertion. Inference.
- RT-1 Table 7 shows that capping to 200 demos per task (half the data) cut unseen-task success from 76 to 52 percent, which is a larger drop than the Lin et al. plateau would predict; the difference is that RT-1's 744 tasks are each heterogeneous, so 200 per instruction does not mean 200 per environment-object condition. Inference.

### Gaps
- Lin et al. Fig. 7 per-point normalized scores (64 to 6,400 demos) are only in the figure.
- robomimic Tables 27 and 28 (20 and 50 percent subsets) were not retrieved.
- pi0 Fig. 11 and pi0.5 Fig. 8 per-point values are only in figures.
- Octo was not checked for a data-size ablation in this pass.
- No general study reports a fitted exponent for demonstrations per task on hardware; Factored Scaling Curves fits one but does not publish its coefficients.

## Key question 4: Minimum demonstrations per task to reach 80 percent success, and the trade-off between environment or object diversity and demonstrations per environment

### Takeaway
No paper states a universal minimum. The empirical floor for 80 percent success on a single-scene pick-and-place task with a modern imitation policy is about 50 demonstrations (Lin et al. recommend 50 per environment-object pair; Diffusion Policy reaches 82 percent on robomimic Can at 50 demos; OmniClone plus GR00T N1.6 reaches 80 to 86 percent with 50 whole-body demos on the G1; HumanoidExo reaches 80 percent with 200 teleop demos or 5 teleop plus 195 exoskeleton demos). Generalization to new scenes and objects is governed by the number of distinct environments and objects, not by demos per environment: Lin et al. show overlapping curves at 25 to 100 percent of demos per environment, RT-1 shows that cutting 25 percent of tasks hurts as much as cutting 49 percent of episodes, and pi0.5 shows 104 locations matching a policy trained in the test home.

### Cited Findings
- Lin et al.: "collecting 50 demonstrations per environment-object pair (K = 50) for tasks of similar difficulty"; 32 pairs times 50 demos yields 85.0 to 92.5 percent success in unseen environments with unseen objects; 8 objects already give normalized score above 0.8; beyond about 16 environments, one object per environment suffices. [Sec. 4.3, Table 1, Fig. 2, Fig. 6](https://arxiv.org/abs/2410.18647)
- Lin et al.: "expanding the diversity of environments and objects is more effective than merely increasing the number of demonstrations for each individual environment or object"; 50 percent and 100 percent demo-fraction curves overlap for environment scaling, 25 percent and 100 percent overlap for env-object scaling. [Sec. 4.1, Figs. 3 and 4](https://arxiv.org/abs/2410.18647)
- RT-1: narrowing tasks by 25 percent while keeping 97 percent of data gives unseen-task success 67 percent vs 76 percent for full data, matching the effect of removing 49 percent of episodes (52 percent); "data diversity is more essential than data quantity". [Table 7, Sec. 6.5](https://arxiv.org/abs/2212.06817)
- robomimic: Lift and Can reach "75 to 100 percent success rate" with 20 percent of 200 demos (40 demos); Square needs the full 200 to reach 84 percent; Tool Hang reaches only 19.3 percent at 200. [Table 1 and text](https://arxiv.org/abs/2108.03298)
- Waypoint Table 2 (Diffusion Policy, image obs): Can crosses 80 percent at 50 demos (82.3 percent), Square at 100 demos (82.0 percent); Lift is 100 percent at 30. [Table 2](https://arxiv.org/abs/2307.14326)
- GR00T N1 on the real GR-1: 10 percent of a 15 min to 3 h per-task dataset gives 42.6 percent average; the full set gives 76.8 percent; only Pick-and-Place seen (92.0), Cylinder Handover (86.6), Coordination 1 and 2 (80.0, 85.0) exceed 80 percent at full data. [Tables 3 and 5](https://arxiv.org/abs/2503.14734)
- GR00T N1.5 on the G1: 1,000 teleop episodes give 98.8 percent on seen fruits and 84.2 percent on unseen objects. [GEAR N1.5 page, Table 3](https://research.nvidia.com/labs/gear/gr00t-n1_5/)
- OmniClone plus GR00T N1.6 on the G1: 50 whole-body demos give 85.71 percent (21 trials) and 80.00 percent (5 trials). [Table II](https://arxiv.org/abs/2603.14327)
- HumanoidExo on the G1: 5 teleop demos give 5 percent; 200 teleop demos give 80 percent; 5 teleop plus 195 exoskeleton demos give 80 percent (seen cloth) and 75 percent (unseen cloth). [Table 1](https://arxiv.org/abs/2510.03022)
- OmniH2O on the H1: Squat reaches 9/10 at 25 percent of about 5 min of data; Rock-Paper-Scissors reaches 9/10 at 50 percent; Catch-Release reaches only 6/10 at 100 percent. [Table 17a](https://arxiv.org/abs/2406.08858)
- pi0.5: generalization in unseen homes improves with 3 to 104 training locations, and the 104-location model matches a control trained on the test homes. [Fig. 8](https://arxiv.org/abs/2504.16054)
- pi0: 5 h of fine-tuning data for the simplest tasks and 100 or more hours for the most complex. [Sec. V-A](https://arxiv.org/abs/2410.24164)
- LingBot-VLA: 80 demos per task beats pi0.5 at 130 demos per task after large pretraining. [Fig. 6](https://arxiv.org/abs/2601.18692)
- lambda-0: 50 robot demos give 60.0 percent mean task score vs 53.3 percent for 200 human demos on two G1 tasks, at 76.4 percent less labor per demo for human capture. [Fig. 9, Sec. 5.1](https://arxiv.org/abs/2610.18950)
- Scaling Single Human Demonstrations: 3 to 5 object meshes adds 5.2 percent while 600 to 800 demos adds 1.1 percent. [Fig. 3](https://arxiv.org/abs/2602.12734)
- ExBody2 (tracking, not task success): a 250-clip feasible, upper-body-diverse subset beats the 1,919-clip raw set on OOD ACCAD MPJPE (0.1421 vs 0.1780 rad), supporting diversity-with-feasibility over volume for RL trackers. [Table X(c)](https://arxiv.org/abs/2412.13196)

### Inferences
- For the Vicon-to-G1 household-task pipeline, the evidence supports planning about 50 demonstrations per task per environment-object condition for the autonomous (VLA or Diffusion Policy) layer, and spending additional collection budget on new objects and placements rather than on more repetitions in one setup. This follows Lin et al. and is consistent with OmniClone's 50-demo result on the same robot. Inference.
- The 80 percent threshold is reached on hardware with 50 to 200 demos for quasi-static pick-and-place on the G1 and H1, but no humanoid study shows a dynamic or contact-rich task above 80 percent with fewer than several hundred demos (OmniH2O Catch-Release stays at 60 percent). Inference.
- Diversity scaling (environments, objects, locations) follows a power law with exponent magnitude roughly 0.5 to 0.8 in the one study that fit it; demonstrations per condition saturate at about 50. Collection budgets should therefore be allocated as (number of conditions) times 50, with conditions chosen to span the deployment distribution. Inference from Lin et al.

### Gaps
- No humanoid paper fits demonstrations-per-task to success; the 80 percent thresholds above are read off two- or three-point comparisons.
- Trial counts in several humanoid hardware studies are small (OmniClone Squat task 5 trials; OmniH2O 10 runs per cell), so the success-rate resolution is 10 to 20 percentage points.
- No study was found that varies environment diversity on a humanoid; the diversity evidence is from tabletop arms (Lin et al., RT-1), mobile manipulators (pi0.5) and simulation (Scaling Single Human Demonstrations).
- Whether the 50-demo rule transfers from UMI handheld-gripper data to whole-body humanoid teleoperation is untested; OmniClone's 50-demo result is a single data point with no sweep.
