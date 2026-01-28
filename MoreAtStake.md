More at Stake: How Payoff and Language Shape LLM Agent Strategies in
Cooperation Dilemmas
Trung-Kiet Huynh1,3,†
, Dao-Sy Duy-Minh1,3,†
, Thanh-Bang Cao2,3
, Phong-Hao
Le2,3
, Hong-Dan Nguyen2,3
and Nguyen Lam Phu Quy1,3
, Minh-Luan Nguyen-Vo2,3
, Hong-Phat
Pham2,3
, Pham Phu Hoa1,3
, Thien-Kim Than2,3
and Chi-Nguyen Tran2,3
, Huy
Tran2,3
, Gia-Thoai Tran-Le2,3
, Alessio Buscemi4
, Le Hong Trang2,3,⋆
, The Anh Han5,⋆
1Faculty of Information Technology, University of Science (HCMUS), Vietnam
2Faculty of Computer Science and Engineering, Ho Chi Minh City University of Technology (HCMUT),
Vietnam
3Vietnam National University - Ho Chi Minh City (VNU-HCM), Vietnam
4Luxembourg Institute of Science and Technology, Luxembourg
5School of Computing, Engineering and Digital Technologies, Teesside University, UK
†Equal Contribution, ⋆Corresponding authors
23122039@student.hcmus.edu.vn, 23122041@student.hcmus.edu.vn, bang.caothanh455@hcmut.edu.vn,
hao.lephong@hcmut.edu.vn, nhdan.sdh232@hcmut.edu.vn, 23122048@student.hcmus.edu.vn,
luan.nguyenvm@hcmut.edu.vn, phat.phamhong@hcmut.edu.vn, 23122030@student.hcmus.edu.vn,
kim.thanthien04@hcmut.edu.vn, 23122044@student.hcmus.edu.vn, tranhuy@hcmut.edu.vn,
thoai.trantlgt2610@hcmut.edu.vn, t.han@tees.ac.uk, lhtrang@hcmut.edu.vn
Abstract
1 As LLMs increasingly act as autonomous agents
2 in interactive and multi-agent settings, understand3 ing their strategic behavior is critical for safety,
4 coordination, and AI-driven social and economic
5 systems. We investigate how payoff magnitude
6 and linguistic context shape LLM strategies in re7 peated social dilemmas, using a payoff-scaled Pris8 oner’s Dilemma to isolate sensitivity to incentive
9 strength. Across models and languages, we observe
10 consistent behavioral patterns, including incentive11 sensitive conditional strategies and cross-linguistic
12 divergence. To interpret these dynamics, we train
13 supervised classifiers on canonical repeated-game
14 strategies and apply them to LLM decisions, reveal15 ing systematic, model- and language-dependent be16 havioral intentions, with linguistic framing some17 times matching or exceeding architectural effects.
18 Our results provide a unified framework for audit19 ing LLMs as strategic agents and highlight cooper20 ation biases with direct implications for AI gover21 nance and multi-agent system design.
22 1 Introduction
23 Large language models (LLMs) are increasingly deployed
24 as agents in recommendation systems, negotiation tools, and
25 multi-agent assistants [Tessler et al., 2024; Hammond et al.,
26 2025]. In these settings, LLMs face cooperation dilemmas
27 in which behavior emerges from strategic interactions rather
28 than isolated model outputs. Empirical studies show that
such behavior is shaped by training, prompting, role assign- 29
ment, and linguistic framing, with direct implications for 30
safety, coordination, and AI governance [Lu et al., 2024; 31
Akata et al., 2025; Fontana et al., 2025]. Equally critical 32
is the adaptability of their cooperative strategies to varying 33
costs and benefits (payoff stakes), as this directly influences 34
AI system outcomes across a spectrum of real-world scenar- 35
ios [Hammond et al., 2025]. 36
A growing body of work evaluates LLMs through game- 37
theoretic lenses, particularly via matrix and repeated games, 38
revealing systematic departures from Nash equilibria, per- 39
sistent cooperative biases, and sensitivity to contextual fac- 40
tors such as language and incentives [Akata et al., 2025; 41
Sun and others, 2025; Mao et al., 2025; Pal et al., 2026; 42
Willis et al., 2025; Fan et al., 2024; Pires et al., 2025]. 43
FAIRGAME [Buscemi et al., 2025b] provides a controlled 44
experimental framework for probing these effects across 45
models, languages, and personalities. However, most exist- 46
ing evaluations focus on aggregate outcomes, such as cooper- 47
ation rates or payoff distributions, and do not directly model 48
the behavioral intentions underlying observed actions. 49
Evaluating strategic behavior at the level required for gov- 50
ernance and alignment therefore demands methods that go 51
beyond surface-level outputs. Drawing on behavioral and 52
evolutionary game theory, we conceptualize behavioral in- 53
tention as an agent’s strategy: a decision rule mapping in- 54
teraction histories to subsequent actions [Han et al., 2011; 55
Di Stefano et al., 2023; Han et al., 2012; Fujimoto and 56
Kaneko, 2019]. Classical canonical strategies in repeated 57
games, such as Always Cooperate (ALLC), Always De- 58
fect (ALLD), Tit-for-Tat (TFT), and Win-Stay–Lose-Shift 59
(WSLS) [Axelrod, 1980; Sigmund, 2010], provide an in- 60
61 terpretable vocabulary for such intentions. Prior work has
62 shown that these strategies can be inferred from noisy behav63 ioral trajectories using supervised learning [Han et al., 2011;
64 Di Stefano et al., 2023], and extended using probabilistic
65 models to capture mixed or stochastic behavior [Montero66 Porras et al., 2022].
67 In parallel, recent studies highlight that LLM behavior
68 is not invariant across languages [Buscemi et al., 2025b].
69 Strategic reasoning, risk sensitivity, and cooperation patterns
70 have been shown to depend on linguistic framing, sometimes
71 with effects comparable in magnitude to architectural differ72 ences [Lorè and Heydari, 2024; Buscemi et al., 2025a]. This
73 raises the question of whether behavioral intentions (or strate74 gies used by LLM agents) inferred from gameplay are them75 selves language-dependent, and whether such dependencies
76 introduce systematic biases in multi-agent settings.
77 This work builds on and extends these strands of research.
78 Our experimental design incorporates a payoff-scaled Pris79 oner’s Dilemma that systematically varies the stakes (i.e.
80 magnitude) of cooperation while preserving the underlying
81 strategic structure. Moreover, using synthetic repeated-game
82 trajectories [Han et al., 2011], we train supervised inten83 tion classifiers and apply them to LLM-generated gameplay
84 logs to infer canonical strategies. This allows us to address
85 two important questions: 1) Do LLM agents systematically
86 change cooperative behavior as payoff stakes vary, and how
87 does this differ across models and languages? 2) Can LLM
88 behavioral intentions be reliably classified using supervised
89 learning, and what systematic biases emerge across models
90 and languages?
91 Our approach complements and extends recent long92 horizon studies of repeated games with LLMs. In particu93 lar, Fontana et al. [Fontana et al., 2025] analyse 100-round
94 interactions and introduce the Strategy Frequency Estima95 tion Method (SFEM) to recover rich strategic archetypes, in96 cluding Grim Trigger, Generous Tit-for-Tat, and extortion97 ate strategies, achieving high population-level accuracy. Our
98 approach employs a 10-round horizon, which is designed to
99 enable direct exploration of payoff-scaling and multilingual
100 effects - the core contextual factors of our study. This de101 sign, while trading off the capacity to discern complex, multi102 stage conditional strategies, allows us to obtain highly inter103 pretable, pointwise estimates of canonical intentions.
104 Finally, while human behavioral baselines in repeated Pris105 oner’s Dilemma are well studied [Montero-Porras et al.,
106 2022; Akata et al., 2025; Axelrod, 1980; Krockow et al.,
107 2016], systematic comparisons under matched experimental
108 conditions remain largely absent from LLM evaluations. Hu109 man cooperation rates and strategy distributions vary with in110 centives, culture, and framing. Our findings of incentive and
111 payoff-stakes sensitive cooperation and cross-linguistic diver112 gence echo these patterns, but without direct human base113 lines, we do not claim behavioral equivalence. Instead, we
114 position intention classification as a diagnostic tool for iden115 tifying systematic structure and bias in LLM strategic be116 havior, providing a foundation for future comparative and
117 governance-oriented analyses.
2 Methodology 118
2.1 Framework 119
FAIRGAME (Framework for AI Agents Bias Recognition 120
using Game Theory) [Buscemi et al., 2025b] provides our 121
computational infrastructure. The framework supports sys- 122
tematic, reproducible LLM evaluations through controlled 123
game-theoretic experiments. Experimental conditions are de- 124
fined via JSON configuration files specifying payoff struc- 125
tures, game horizon, LLM backends, and languages. At run- 126
time, FAIRGAME combines configurations with language- 127
specific prompt templates, simulates repeated normal-form 128
games, and logs round-by-round trajectories. We extend 129
FAIRGAME with payoff-scaling for the Prisoner’s Dilemma 130
to investigate LLM sensitivity to incentive magnitude. 131
2.2 Payoff stakes: scaled payoff matrix 132
We first examine the sensitivity of LLM agents to the abso- 133
lute magnitude of incentives in a dyadic setting. To this end, 134
we use a repeated Prisoner’s Dilemma in which only the nu- 135
merical values of the payoffs are scaled, while the underlying 136
strategic structure of the game is kept fixed. In this way, the 137
“stakes” of the interaction are varied without changing best 138
responses or the ranking of outcomes. It has been shown, 139
theoretically [Han et al., 2021] and empirically in human ex- 140
periments [Krockow et al., 2016; List, 2006], that cooper- 141
ative behaviors are strongly influenced by this factor. This 142
design connects to recent work on workflow-guided rational- 143
ity and opponent shaping in LLM agents [Hua et al., 2024], 144
where stake magnitude may interact with learned policies to 145
produce non-trivial behavioral shifts. The row player’s base- 146
line payoff matrix is given by
(A, A) 7→ (6, 6), (A, B) 7→ 147
(0, 10), (B, A)7→(10, 0), (B, B)7→(2, 2)
, where Option A 148
denotes defection and Option B cooperation. The agents’ ob- 149
jective is to minimise their cumulative penalties. Thus, mutual 150
cooperation (B,B) yields the lowest combined penalty (2,2), 151
while mutual defection (A,A) yields higher penalties (6,6). 152
Under the penalty framing, the matrix satisfies the ordering 153
T(0) < R(2) < P(6) < S(10), where T (Temptation: de- 154
fecting while opponent cooperates) yields the lowest penalty, 155
followed by R (Reward: mutual cooperation), P (Punish- 156
ment: mutual defection), and S (Sucker: cooperating while 157
opponent defects). Note that in standard reward framing, the 158
ordering is inverted (T > R > P > S); our penalty fram- 159
ing preserves the PD incentive structure where defection is 160
individually dominant. To manipulate the stakes of the game 161
without altering its strategic structure, we introduce a scalar 162
parameter λ > 0 and multiply all penalties by λ [Han et 163
al., 2021]. In our experiments we consider three values – 164
λ ∈ {0.1, 1.0, 10.0} – corresponding to attenuated, baseline, 165
and amplified payoff magnitudes (e.g., mutual cooperation 166
yields penalties of 0.2, 2, and 20 respectively). The payoff 167
ordering is preserved in all cases, isolating the effect of pay- 168
off magnitude while keeping the underlying game-theoretic 169
incentives unchanged. 170
Two-player games between LLM agents are run us- 171
ing FAIRGAME as the simulation engine [Buscemi et al., 172
2025b]. Each game is played for a fixed, finite horizon 173
of N = 10 rounds; following the known-horizon condi- 174
175 tion from the FAIRGAME protocol, agents are explicitly in176 formed of the total number of rounds in the prompt, which
177 may drive end-game defection patterns consistent with back178 ward induction in finite repeated games [Sigmund, 2010].
179 End-game effects are evident: defection rates in rounds 9–
180 10 exceed those in rounds 1–8 across all conditions, con181 sistent with backward-induction reasoning. The unknown182 horizon condition, where agents are not informed of the game
183 length, remains an avenue for future investigation. In every
184 round both agents observe the full public history of past ac185 tions and payoffs before choosing their next move. Agents
186 do not communicate outside of their action choices. For
187 each parameter configuration, we simulate multiple indepen188 dent runs (10 repetitions per condition) to account for the
189 stochasticity of LLM outputs. We evaluate three LLM back190 ends: GPT-4o [Hurst et al., 2024] (temperature: 1.0, top_p:
191 1.0), Claude 3.5 Haiku [Anthropic, 2024] (temperature: 1.0,
192 top_p: 1.0), and Mistral Large [Jiang et al., 2023] (temper193 ature: 0.3, top_p: 1.0). Following the FAIRGAME proto194 col [Buscemi et al., 2025b], we adopt each provider’s rec195 ommended default settings rather than standardising across
196 models. This design choice reflects realistic deployment
197 conditions: practitioners typically use models “out of the
198 box” with vendor-recommended configurations, and our be199 havioral findings thus generalize to practical multi-agent ap200 plications. While temperature differences (GPT-4o/Claude:
201 1.0; Mistral: 0.3) may introduce variability confounds, prior
202 FAIRGAME analyses demonstrate that key behavioral pat203 terns (cross-linguistic divergence, personality effects) persist
204 across models despite differing temperature settings; con205 trolled temperature ablations remain an avenue for future
206 work.
207 To examine potential cross-lingual effects, the same game
208 is instantiated in five languages: English, French, Arabic,
209 Mandarin Chinese, and Vietnamese. Prompt templates were
210 translated by native speakers with back-translation verifica211 tion to ensure semantic and numeric equivalence across lan212 guages; all templates explicitly instruct agents that lower
213 penalties are better outcomes, verified through independent
214 review by native speakers to avoid misinterpretation; tem215 plates will be released with the code. Agent roles (first/second
216 mover) were randomized across runs to control for positional
217 bias. In all conditions, neutral framing is employed: “Op218 tion A” corresponds to defection and “Option B” to coop219 eration, and the prompt does not contain any explicit moral
220 or normative language. Personality traits, cooperative (C)
221 or selfish (S), are systematically varied across agent pairings
222 (CC, CS, SC, SS). In total, we run 3 models × 5 languages ×
223 3 λ values × 4 personality pairings × 10 repetitions = 1, 800
224 games, yielding 36,000 agent decisions (each game produces
225 20 decisions across N=10 rounds for 2 agents).
226 2.3 LLM behavioral intention recognition
227 While the FAIRGAME framework provides complete game228 play trajectories and descriptive metrics such as cooperation
229 rates and payoff sensitivities, these primarily capture what
230 agents do rather than why they behave that way. Our goal is
231 to uncover the latent behavioral intentions embedded within
232 these decision sequences to better interpret the motivations
behind agents’ actions and understand how LLM strategies 233
differ from human strategies. 234
Building on prior work by Han et al. [Han et al., 2012; 235
Han et al., 2011] and Di Stefano et al.[Di Stefano et al., 236
2023], which demonstrated how to infer canonical strategies 237
from large-scale repeated gameplay data by incorporating ex- 238
ecution noise (ϵ) to replicate stochasticity, we adopted and 239
adapted this methodology. Our objective is to apply this ap- 240
proach to classify the underlying behavioral intentions exhib- 241
ited by LLMs during their gameplay turns. Figure 1 illus- 242
trates the pipeline we employed, detailing how this intention 243
prediction model was adapted to analyse the outputs of the 244
FAIRGAME framework. 245
Sequence
of actions
Noise
level
TFT
ALLC
ALLD
WSLS
Neural
Network
Logistic
Regression
Random
Forest
TRAINING PHASE
INFERENCE PHASE
FAIRGAME
Framework
Chosen
Model
Choosing
the best
model
Sequence
of actions
Low-confidence
p < 0.9
High-confidence
p >= 0.9
Inferred Intentions
LSTM
Figure 1: Supervised Learning Pipeline for Understanding LLM
behavior. Starting from action sequences associated with canonical strategies (ALLC, ALLD, TFT, WSLS) under varying noise
conditions, we train supervised learning models to infer and classify underlying behavioral intentions. We then apply the bestperforming model to the LLM repeated gameplay data generated by
FAIRGAME. High-confidence predictions (>0.9) are used to identify which strategies the LLM adopts, whereas low-confidence cases
are reserved for subsequent analysis to investigate the possibility of
emerging behaviors by the LLM.
Following [Di Stefano et al., 2023], we generate 10,000 246
synthetic trajectories (2,500 per strategy, balanced) for four 247
canonical strategies: TFT, ALLC, ALLD, and WSLS [Sig- 248
mund, 2010] (see Supplementary Material, Section 1.3 for 249
formal definitions). Each trajectory spans 10 rounds against 250
a random opponent, with execution noise (ϵ ∈ {0, 0.05}) 251
injected to simulate LLM stochasticity. We train Logis- 252
tic Regression [Cox, 1958], Random Forests [Breiman, 253
2001], Neural Networks [Jordan and Bishop, 1996], and 254
LSTM [Hochreiter and Schmidhuber, 1997] classifiers, se- 255
lecting the best-performing model for downstream inference. 256
FAIRGAME logs are preprocessed into state-action se- 257
quences encoding interaction outcomes: Reward (R), Pun- 258
ishment (P), Temptation (T), and Sucker (S). The trained 259
model outputs probability distributions over strategy classes; 260
we focus on high-confidence predictions (>0.9) to ensure re- 261
liability. 262
263 3 Results
264 3.1 Payoff magnitude sensitivity
265 The results in this subsection are based on the payoff-scaled
266 Prisoner’s Dilemma experiments described in Section 2.2.
267 These experiments evaluate three LLM models (GPT-4o,
268 Claude 3.5 Haiku, and Mistral Large) across five languages
269 (Arabic, Chinese, English, French, and Vietnamese) under
270 three payoff scaling conditions (λ ∈ {0.1, 1.0, 10.0}). Fol271 lowing the FAIRGAME framework [Buscemi et al., 2025b],
272 the payoff matrix represents penalties (years of imprisonment
273 in the Prisoner’s Dilemma narrative), where lower values in274 dicate better outcomes for agents. The agents’ objective is
275 to minimize their cumulative penalties over the course of the
276 repeated game. Figure 2 displays bar plots summarising the
277 total penalties incurred by agents in the Prisoner’s Dilemma
278 game, with 95% Confidence Intervals computed via per-run
279 aggregation: each run yields one total penalty, and Confi280 dence Intervals are estimated by bootstrapping across the 10
281 independent repetitions per condition. These totals are com282 puted from the test results and grouped by the payoff-scaling
283 parameter λ, language, and personality pairings. In the de284 fault FAIRGAME configuration, each agent is assigned one
285 of two personalities: Cooperative (C) or Selfish (S), resulting
286 in four possible ordered pairings (CC, CS, SC, SS). For visu287 alisation, the asymmetric pairings CS and SC are grouped as
288 mixed since they exhibit symmetric aggregate behavior.
289 Because the payoff matrix is scaled by λ, the range of to290 tal penalties scales accordingly. To enable cross-scale com291 parison, we define the normalized penalty ratio as the to292 tal penalty divided by the worst-case individual penalty (the
293 “sucker” outcome, S = 10λ per round, times N rounds).
294 Thus, values closer to 1 indicate worse outcomes.
295 Figure 2 shows that agents in the attenuated payoff set296 ting (i.e., λ = 0.1) often exhibit higher defection rates, re297 sulting in worse normalized outcomes. This indicates that
298 when the stakes of the game are attenuated, defection be299 comes more frequent, consistent with game-theoretic predic300 tions that low stakes lead to more unconditional defection
301 [Han et al., 2021]. Within each language, the baseline and
302 amplified payoff settings yield broadly similar patterns.
303 When comparing languages, the results indicate that LLMs
304 are sensitive to their linguistic context. For instance, cooper305 ative pairings for models like Mistral led to the highest de306 fection rates in Arabic, Chinese, and Vietnamese. In contrast,
307 selfish and mixed pairings tend to result in more defection for
308 English and French. Notably, a distinct reversal of behavior
309 was observed between English and Vietnamese: models that
310 yielded lower total penalties in English often produced higher
311 penalties in Vietnamese, and vice versa, showing the clear in312 fluence of language on LLM decisions.
313 Figure 3 presents round-by-round choice trajectories.
314 Claude 3.5 Haiku learns to cooperate over time, with
315 attenuated-stake trajectories favouring defection. GPT-4o ex316 hibits the opposite trend, converting to more defective behav317 ior over time, especially for the higher payoff stakes. Mis318 tral Large shows a different trend, with amplified payoffs cor319 relating with increased defection-consistent with dominant
320 strategy reasoning. A notable spike at Round 2 in Mistral’s
trajectories suggests retaliatory or probing behavior [Akata et 321
al., 2025]. 322
Our additional analysis (Supplementary Material, Figure 323
A3) reveals that varying payoff stakes strongly impact LLM 324
behavioral characteristics [Buscemi et al., 2025b], particu- 325
larly their internal variability (the variance of outcomes when 326
the same game scenario is played multiple times). 327
3.2 LLM strategies in repeated games 328
We apply the intent recognition framework (see Section 2.3) 329
to LLMs decision trajectories to examine how their inferred 330
strategic intentions vary with incentive magnitude, linguistic 331
context, and model architecture. Before applying our classifi- 332
cation framework to unknown LLM trajectories, we validated 333
its robustness against synthetic baselines. This step is critical 334
to differentiate between genuine strategic shifts and artifacts 335
of classification error. 336
Figure 4 confirms the LSTM maintains robust performance 337
even as the strategy space expands, successfully distinguish- 338
ing between behaviorally similar conditional strategies (i.e. 339
TFT and WSLS) within our analyzed set of four canonical 340
strategies (including ALLC and ALLD; see Supplementary 341
Material, Section 1.3 for details) [Sigmund, 2010]. The re- 342
current architecture’s ability to filter execution noise com- 343
mon in LLM outputs makes it particularly well-suited for this 344
task [Di Stefano et al., 2023]. 345
We use a hybrid classification pipeline combining rule- 346
based pattern matching for unambiguous trajectories with 347
LSTM predictions for complex cases. Of the 3,600 agent 348
trajectories (2 agents × 1,800 games), approximately 90% 349
achieved classification confidence >0.9 and were retained for 350
analysis. Details on threshold sensitivity are provided in the 351
Supplementary Material, Section 1.5. 352
Table 1 shows the aggregate and model-specific strategy 353
distributions across all experimental conditions. Three pat- 354
terns emerge. First, conditional strategies (WSLS and TFT) 355
account for nearly half of all trajectories, almost matching 356
unconditional strategies. This contrasts with game theory, 357
which predicts universal defection in finite-horizon games via 358
backward induction [Sigmund, 2010; Axelrod, 1980]. LLMs 359
instead use heuristics that respond to recent history, similar 360
to bounded rationality in human players [Akata et al., 2025; 361
Han et al., 2012; Lu et al., 2024]. Second, a moderate coop- 362
erative bias is evident: ALLC is more frequent than ALLD, 363
consistent across payoff scales, languages, and models. This 364
likely reflects alignment training, such as Reinforcement 365
Learning from Human Feedback (RLHF) and Constitutional 366
AI, optimising for prosocial behavior [Ouyang et al., 2022; 367
Bai et al., 2022; Buscemi et al., 2025c]. Third, strategic 368
heterogeneity is high: distribution entropy approaches the 369
theoretical maximum, indicating diverse strategic repertoires. 370
This validates intent classification: aggregate cooperation 371
rates alone would conflate fundamentally different decision 372
rules [Di Stefano et al., 2023; Han et al., 2012]. 373
Figure 5 shows how strategy distributions shift with payoff 374
scaling. As λ increases from 0.1 to 10, we observe a clear be- 375
havioral inversion: unconditional defection (ALLD) sharply 376
declines, effectively halving its prevalence, while conditional 377
cooperation (WSLS) and unconditional cooperation (ALLC) 378
0
200
400
600
High
English French Arabic Chinese Vietnamese
0
20
40
60
Ordinary
CC CS SS
0
2
4
6
Very low
CC CS SS CC CS SS CC CS SS CC CS SS
Claude 3.5 Haiku GPT-4o Mistral Large
Figure 2: Aggregated final penalties across repeated Prisoner’s Dilemma games, presented for each LLM under different payoff scales. Results
are reported for five languages, and evaluated across the payoff-scaling parameters λ ∈ {0.1, 1.0, 10.0}, which correspond to attenuated (top
row), baseline (middle row), and amplified penalty scales (bottom row), respectively.
2 4 6 8 10
Round Number
Option B (-1)
-0.5
0
0.5
Option A (1)
Average Strategy Value
Claude 3.5 Haiku
Exponential Value
High
Ordinary
Very low
2 4 6 8 10
Round Number
GPT-4o
2 4 6 8 10
Round Number
Mistral Large
Figure 3: Average trajectory of strategy choices across repeated
rounds in all Prisoner’s Dilemma experiments, shown for each LLM
under different payoff magnitudes. A value of 1 indicates selection
of Option A (defection), while −1 corresponds to Option B (cooperation). The experiments consider λ ∈ {0.1, 1.0, 10.0}, representing
attenuated, baseline, and amplified penalty scales, respectively. The
blue line denotes the standard payoff matrix (λ = 1.0), the red line
reflects the payoff matrix scaled by 10 (λ = 10.0), and the green
line represents the payoff matrix scaled by 0.1 (λ = 0.1).
379 both see marked increases. Tit-for-Tat (TFT) remains rela380 tively stable across conditions. This pattern strongly aligns
381 with standard stake-effect predictions: low stakes promote
382 exploratory, risk-seeking behavior, while higher stakes in383 duce commitment to stable, mutually beneficial conventions
384 [Han et al., 2021; Sigmund, 2010]. The substantial shift
385 from ALLD to WSLS as payoff stake rises implies that LLM
386 agents are not statically aligned but modulate their strate387 gic commitments based on incentive salience, transitioning
388 from opportunistic defection toward adaptive reciprocity as
389 the consequences of error become more severe.
390 Table 1 shows model-specific strategy distributions.
391 Claude 3.5 Haiku displays a cooperative strategic profile,
392 with the highest level of overall cooperation (ALLC + WSLS
3 Strategies 4 Strategies 5 Strategies
Model Configuration
0.5
0.6
0.7
0.8
0.9
1.0
Score
LSTM Model Performance Comparison
Accuracy
Precision
Recall
F1-Score
Figure 4: LSTM intent recognizer performance. F1 ranges from
0.78 (5-strategy) to 0.984 (4-strategy) on 5% noise data; all subsequent analyses use the 4-strategy classifier (F1=0.984).

More at Stake: How Payoff and Language Shape LLM Agent Strategies in
Cooperation Dilemmas
Trung-Kiet Huynh1,3,†
, Dao-Sy Duy-Minh1,3,†
, Thanh-Bang Cao2,3
, Phong-Hao
Le2,3
, Hong-Dan Nguyen2,3
and Nguyen Lam Phu Quy1,3
, Minh-Luan Nguyen-Vo2,3
, Hong-Phat
Pham2,3
, Pham Phu Hoa1,3
, Thien-Kim Than2,3
and Chi-Nguyen Tran2,3
, Huy
Tran2,3
, Gia-Thoai Tran-Le2,3
, Alessio Buscemi4
, Le Hong Trang2,3,⋆
, The Anh Han5,⋆
1Faculty of Information Technology, University of Science (HCMUS), Vietnam
2Faculty of Computer Science and Engineering, Ho Chi Minh City University of Technology (HCMUT),
Vietnam
3Vietnam National University - Ho Chi Minh City (VNU-HCM), Vietnam
4Luxembourg Institute of Science and Technology, Luxembourg
5School of Computing, Engineering and Digital Technologies, Teesside University, UK
†Equal Contribution, ⋆Corresponding authors
23122039@student.hcmus.edu.vn, 23122041@student.hcmus.edu.vn, bang.caothanh455@hcmut.edu.vn,
hao.lephong@hcmut.edu.vn, nhdan.sdh232@hcmut.edu.vn, 23122048@student.hcmus.edu.vn,
luan.nguyenvm@hcmut.edu.vn, phat.phamhong@hcmut.edu.vn, 23122030@student.hcmus.edu.vn,
kim.thanthien04@hcmut.edu.vn, 23122044@student.hcmus.edu.vn, tranhuy@hcmut.edu.vn,
thoai.trantlgt2610@hcmut.edu.vn, t.han@tees.ac.uk, lhtrang@hcmut.edu.vn
Abstract
1 As LLMs increasingly act as autonomous agents
2 in interactive and multi-agent settings, understand3 ing their strategic behavior is critical for safety,
4 coordination, and AI-driven social and economic
5 systems. We investigate how payoff magnitude
6 and linguistic context shape LLM strategies in re7 peated social dilemmas, using a payoff-scaled Pris8 oner’s Dilemma to isolate sensitivity to incentive
9 strength. Across models and languages, we observe
10 consistent behavioral patterns, including incentive11 sensitive conditional strategies and cross-linguistic
12 divergence. To interpret these dynamics, we train
13 supervised classifiers on canonical repeated-game
14 strategies and apply them to LLM decisions, reveal15 ing systematic, model- and language-dependent be16 havioral intentions, with linguistic framing some17 times matching or exceeding architectural effects.
18 Our results provide a unified framework for audit19 ing LLMs as strategic agents and highlight cooper20 ation biases with direct implications for AI gover21 nance and multi-agent system design.
22 1 Introduction
23 Large language models (LLMs) are increasingly deployed
24 as agents in recommendation systems, negotiation tools, and
25 multi-agent assistants [Tessler et al., 2024; Hammond et al.,
26 2025]. In these settings, LLMs face cooperation dilemmas
27 in which behavior emerges from strategic interactions rather
28 than isolated model outputs. Empirical studies show that
such behavior is shaped by training, prompting, role assign- 29
ment, and linguistic framing, with direct implications for 30
safety, coordination, and AI governance [Lu et al., 2024; 31
Akata et al., 2025; Fontana et al., 2025]. Equally critical 32
is the adaptability of their cooperative strategies to varying 33
costs and benefits (payoff stakes), as this directly influences 34
AI system outcomes across a spectrum of real-world scenar- 35
ios [Hammond et al., 2025]. 36
A growing body of work evaluates LLMs through game- 37
theoretic lenses, particularly via matrix and repeated games, 38
revealing systematic departures from Nash equilibria, per- 39
sistent cooperative biases, and sensitivity to contextual fac- 40
tors such as language and incentives [Akata et al., 2025; 41
Sun and others, 2025; Mao et al., 2025; Pal et al., 2026; 42
Willis et al., 2025; Fan et al., 2024; Pires et al., 2025]. 43
FAIRGAME [Buscemi et al., 2025b] provides a controlled 44
experimental framework for probing these effects across 45
models, languages, and personalities. However, most exist- 46
ing evaluations focus on aggregate outcomes, such as cooper- 47
ation rates or payoff distributions, and do not directly model 48
the behavioral intentions underlying observed actions. 49
Evaluating strategic behavior at the level required for gov- 50
ernance and alignment therefore demands methods that go 51
beyond surface-level outputs. Drawing on behavioral and 52
evolutionary game theory, we conceptualize behavioral in- 53
tention as an agent’s strategy: a decision rule mapping in- 54
teraction histories to subsequent actions [Han et al., 2011; 55
Di Stefano et al., 2023; Han et al., 2012; Fujimoto and 56
Kaneko, 2019]. Classical canonical strategies in repeated 57
games, such as Always Cooperate (ALLC), Always De- 58
fect (ALLD), Tit-for-Tat (TFT), and Win-Stay–Lose-Shift 59
(WSLS) [Axelrod, 1980; Sigmund, 2010], provide an in- 60
61 terpretable vocabulary for such intentions. Prior work has
62 shown that these strategies can be inferred from noisy behav63 ioral trajectories using supervised learning [Han et al., 2011;
64 Di Stefano et al., 2023], and extended using probabilistic
65 models to capture mixed or stochastic behavior [Montero66 Porras et al., 2022].
67 In parallel, recent studies highlight that LLM behavior
68 is not invariant across languages [Buscemi et al., 2025b].
69 Strategic reasoning, risk sensitivity, and cooperation patterns
70 have been shown to depend on linguistic framing, sometimes
71 with effects comparable in magnitude to architectural differ72 ences [Lorè and Heydari, 2024; Buscemi et al., 2025a]. This
73 raises the question of whether behavioral intentions (or strate74 gies used by LLM agents) inferred from gameplay are them75 selves language-dependent, and whether such dependencies
76 introduce systematic biases in multi-agent settings.
77 This work builds on and extends these strands of research.
78 Our experimental design incorporates a payoff-scaled Pris79 oner’s Dilemma that systematically varies the stakes (i.e.
80 magnitude) of cooperation while preserving the underlying
81 strategic structure. Moreover, using synthetic repeated-game
82 trajectories [Han et al., 2011], we train supervised inten83 tion classifiers and apply them to LLM-generated gameplay
84 logs to infer canonical strategies. This allows us to address
85 two important questions: 1) Do LLM agents systematically
86 change cooperative behavior as payoff stakes vary, and how
87 does this differ across models and languages? 2) Can LLM
88 behavioral intentions be reliably classified using supervised
89 learning, and what systematic biases emerge across models
90 and languages?
91 Our approach complements and extends recent long92 horizon studies of repeated games with LLMs. In particu93 lar, Fontana et al. [Fontana et al., 2025] analyse 100-round
94 interactions and introduce the Strategy Frequency Estima95 tion Method (SFEM) to recover rich strategic archetypes, in96 cluding Grim Trigger, Generous Tit-for-Tat, and extortion97 ate strategies, achieving high population-level accuracy. Our
98 approach employs a 10-round horizon, which is designed to
99 enable direct exploration of payoff-scaling and multilingual
100 effects - the core contextual factors of our study. This de101 sign, while trading off the capacity to discern complex, multi102 stage conditional strategies, allows us to obtain highly inter103 pretable, pointwise estimates of canonical intentions.
104 Finally, while human behavioral baselines in repeated Pris105 oner’s Dilemma are well studied [Montero-Porras et al.,
106 2022; Akata et al., 2025; Axelrod, 1980; Krockow et al.,
107 2016], systematic comparisons under matched experimental
108 conditions remain largely absent from LLM evaluations. Hu109 man cooperation rates and strategy distributions vary with in110 centives, culture, and framing. Our findings of incentive and
111 payoff-stakes sensitive cooperation and cross-linguistic diver112 gence echo these patterns, but without direct human base113 lines, we do not claim behavioral equivalence. Instead, we
114 position intention classification as a diagnostic tool for iden115 tifying systematic structure and bias in LLM strategic be116 havior, providing a foundation for future comparative and
117 governance-oriented analyses.
2 Methodology 118
2.1 Framework 119
FAIRGAME (Framework for AI Agents Bias Recognition 120
using Game Theory) [Buscemi et al., 2025b] provides our 121
computational infrastructure. The framework supports sys- 122
tematic, reproducible LLM evaluations through controlled 123
game-theoretic experiments. Experimental conditions are de- 124
fined via JSON configuration files specifying payoff struc- 125
tures, game horizon, LLM backends, and languages. At run- 126
time, FAIRGAME combines configurations with language- 127
specific prompt templates, simulates repeated normal-form 128
games, and logs round-by-round trajectories. We extend 129
FAIRGAME with payoff-scaling for the Prisoner’s Dilemma 130
to investigate LLM sensitivity to incentive magnitude. 131
2.2 Payoff stakes: scaled payoff matrix 132
We first examine the sensitivity of LLM agents to the abso- 133
lute magnitude of incentives in a dyadic setting. To this end, 134
we use a repeated Prisoner’s Dilemma in which only the nu- 135
merical values of the payoffs are scaled, while the underlying 136
strategic structure of the game is kept fixed. In this way, the 137
“stakes” of the interaction are varied without changing best 138
responses or the ranking of outcomes. It has been shown, 139
theoretically [Han et al., 2021] and empirically in human ex- 140
periments [Krockow et al., 2016; List, 2006], that cooper- 141
ative behaviors are strongly influenced by this factor. This 142
design connects to recent work on workflow-guided rational- 143
ity and opponent shaping in LLM agents [Hua et al., 2024], 144
where stake magnitude may interact with learned policies to 145
produce non-trivial behavioral shifts. The row player’s base- 146
line payoff matrix is given by
(A, A) 7→ (6, 6), (A, B) 7→ 147
(0, 10), (B, A)7→(10, 0), (B, B)7→(2, 2)
, where Option A 148
denotes defection and Option B cooperation. The agents’ ob- 149
jective is to minimise their cumulative penalties. Thus, mutual 150
cooperation (B,B) yields the lowest combined penalty (2,2), 151
while mutual defection (A,A) yields higher penalties (6,6). 152
Under the penalty framing, the matrix satisfies the ordering 153
T(0) < R(2) < P(6) < S(10), where T (Temptation: de- 154
fecting while opponent cooperates) yields the lowest penalty, 155
followed by R (Reward: mutual cooperation), P (Punish- 156
ment: mutual defection), and S (Sucker: cooperating while 157
opponent defects). Note that in standard reward framing, the 158
ordering is inverted (T > R > P > S); our penalty fram- 159
ing preserves the PD incentive structure where defection is 160
individually dominant. To manipulate the stakes of the game 161
without altering its strategic structure, we introduce a scalar 162
parameter λ > 0 and multiply all penalties by λ [Han et 163
al., 2021]. In our experiments we consider three values – 164
λ ∈ {0.1, 1.0, 10.0} – corresponding to attenuated, baseline, 165
and amplified payoff magnitudes (e.g., mutual cooperation 166
yields penalties of 0.2, 2, and 20 respectively). The payoff 167
ordering is preserved in all cases, isolating the effect of pay- 168
off magnitude while keeping the underlying game-theoretic 169
incentives unchanged. 170
Two-player games between LLM agents are run us- 171
ing FAIRGAME as the simulation engine [Buscemi et al., 172
2025b]. Each game is played for a fixed, finite horizon 173
of N = 10 rounds; following the known-horizon condi- 174
175 tion from the FAIRGAME protocol, agents are explicitly in176 formed of the total number of rounds in the prompt, which
177 may drive end-game defection patterns consistent with back178 ward induction in finite repeated games [Sigmund, 2010].
179 End-game effects are evident: defection rates in rounds 9–
180 10 exceed those in rounds 1–8 across all conditions, con181 sistent with backward-induction reasoning. The unknown182 horizon condition, where agents are not informed of the game
183 length, remains an avenue for future investigation. In every
184 round both agents observe the full public history of past ac185 tions and payoffs before choosing their next move. Agents
186 do not communicate outside of their action choices. For
187 each parameter configuration, we simulate multiple indepen188 dent runs (10 repetitions per condition) to account for the
189 stochasticity of LLM outputs. We evaluate three LLM back190 ends: GPT-4o [Hurst et al., 2024] (temperature: 1.0, top_p:
191 1.0), Claude 3.5 Haiku [Anthropic, 2024] (temperature: 1.0,
192 top_p: 1.0), and Mistral Large [Jiang et al., 2023] (temper193 ature: 0.3, top_p: 1.0). Following the FAIRGAME proto194 col [Buscemi et al., 2025b], we adopt each provider’s rec195 ommended default settings rather than standardising across
196 models. This design choice reflects realistic deployment
197 conditions: practitioners typically use models “out of the
198 box” with vendor-recommended configurations, and our be199 havioral findings thus generalize to practical multi-agent ap200 plications. While temperature differences (GPT-4o/Claude:
201 1.0; Mistral: 0.3) may introduce variability confounds, prior
202 FAIRGAME analyses demonstrate that key behavioral pat203 terns (cross-linguistic divergence, personality effects) persist
204 across models despite differing temperature settings; con205 trolled temperature ablations remain an avenue for future
206 work.
207 To examine potential cross-lingual effects, the same game
208 is instantiated in five languages: English, French, Arabic,
209 Mandarin Chinese, and Vietnamese. Prompt templates were
210 translated by native speakers with back-translation verifica211 tion to ensure semantic and numeric equivalence across lan212 guages; all templates explicitly instruct agents that lower
213 penalties are better outcomes, verified through independent
214 review by native speakers to avoid misinterpretation; tem215 plates will be released with the code. Agent roles (first/second
216 mover) were randomized across runs to control for positional
217 bias. In all conditions, neutral framing is employed: “Op218 tion A” corresponds to defection and “Option B” to coop219 eration, and the prompt does not contain any explicit moral
220 or normative language. Personality traits, cooperative (C)
221 or selfish (S), are systematically varied across agent pairings
222 (CC, CS, SC, SS). In total, we run 3 models × 5 languages ×
223 3 λ values × 4 personality pairings × 10 repetitions = 1, 800
224 games, yielding 36,000 agent decisions (each game produces
225 20 decisions across N=10 rounds for 2 agents).
226 2.3 LLM behavioral intention recognition
227 While the FAIRGAME framework provides complete game228 play trajectories and descriptive metrics such as cooperation
229 rates and payoff sensitivities, these primarily capture what
230 agents do rather than why they behave that way. Our goal is
231 to uncover the latent behavioral intentions embedded within
232 these decision sequences to better interpret the motivations
behind agents’ actions and understand how LLM strategies 233
differ from human strategies. 234
Building on prior work by Han et al. [Han et al., 2012; 235
Han et al., 2011] and Di Stefano et al.[Di Stefano et al., 236
2023], which demonstrated how to infer canonical strategies 237
from large-scale repeated gameplay data by incorporating ex- 238
ecution noise (ϵ) to replicate stochasticity, we adopted and 239
adapted this methodology. Our objective is to apply this ap- 240
proach to classify the underlying behavioral intentions exhib- 241
ited by LLMs during their gameplay turns. Figure 1 illus- 242
trates the pipeline we employed, detailing how this intention 243
prediction model was adapted to analyse the outputs of the 244
FAIRGAME framework. 245
Sequence
of actions
Noise
level
TFT
ALLC
ALLD
WSLS
Neural
Network
Logistic
Regression
Random
Forest
TRAINING PHASE
INFERENCE PHASE
FAIRGAME
Framework
Chosen
Model
Choosing
the best
model
Sequence
of actions
Low-confidence
p < 0.9
High-confidence
p >= 0.9
Inferred Intentions
LSTM
Figure 1: Supervised Learning Pipeline for Understanding LLM
behavior. Starting from action sequences associated with canonical strategies (ALLC, ALLD, TFT, WSLS) under varying noise
conditions, we train supervised learning models to infer and classify underlying behavioral intentions. We then apply the bestperforming model to the LLM repeated gameplay data generated by
FAIRGAME. High-confidence predictions (>0.9) are used to identify which strategies the LLM adopts, whereas low-confidence cases
are reserved for subsequent analysis to investigate the possibility of
emerging behaviors by the LLM.
Following [Di Stefano et al., 2023], we generate 10,000 246
synthetic trajectories (2,500 per strategy, balanced) for four 247
canonical strategies: TFT, ALLC, ALLD, and WSLS [Sig- 248
mund, 2010] (see Supplementary Material, Section 1.3 for 249
formal definitions). Each trajectory spans 10 rounds against 250
a random opponent, with execution noise (ϵ ∈ {0, 0.05}) 251
injected to simulate LLM stochasticity. We train Logis- 252
tic Regression [Cox, 1958], Random Forests [Breiman, 253
2001], Neural Networks [Jordan and Bishop, 1996], and 254
LSTM [Hochreiter and Schmidhuber, 1997] classifiers, se- 255
lecting the best-performing model for downstream inference. 256
FAIRGAME logs are preprocessed into state-action se- 257
quences encoding interaction outcomes: Reward (R), Pun- 258
ishment (P), Temptation (T), and Sucker (S). The trained 259
model outputs probability distributions over strategy classes; 260
we focus on high-confidence predictions (>0.9) to ensure re- 261
liability. 262
263 3 Results
264 3.1 Payoff magnitude sensitivity
265 The results in this subsection are based on the payoff-scaled
266 Prisoner’s Dilemma experiments described in Section 2.2.
267 These experiments evaluate three LLM models (GPT-4o,
268 Claude 3.5 Haiku, and Mistral Large) across five languages
269 (Arabic, Chinese, English, French, and Vietnamese) under
270 three payoff scaling conditions (λ ∈ {0.1, 1.0, 10.0}). Fol271 lowing the FAIRGAME framework [Buscemi et al., 2025b],
272 the payoff matrix represents penalties (years of imprisonment
273 in the Prisoner’s Dilemma narrative), where lower values in274 dicate better outcomes for agents. The agents’ objective is
275 to minimize their cumulative penalties over the course of the
276 repeated game. Figure 2 displays bar plots summarising the
277 total penalties incurred by agents in the Prisoner’s Dilemma
278 game, with 95% Confidence Intervals computed via per-run
279 aggregation: each run yields one total penalty, and Confi280 dence Intervals are estimated by bootstrapping across the 10
281 independent repetitions per condition. These totals are com282 puted from the test results and grouped by the payoff-scaling
283 parameter λ, language, and personality pairings. In the de284 fault FAIRGAME configuration, each agent is assigned one
285 of two personalities: Cooperative (C) or Selfish (S), resulting
286 in four possible ordered pairings (CC, CS, SC, SS). For visu287 alisation, the asymmetric pairings CS and SC are grouped as
288 mixed since they exhibit symmetric aggregate behavior.
289 Because the payoff matrix is scaled by λ, the range of to290 tal penalties scales accordingly. To enable cross-scale com291 parison, we define the normalized penalty ratio as the to292 tal penalty divided by the worst-case individual penalty (the
293 “sucker” outcome, S = 10λ per round, times N rounds).
294 Thus, values closer to 1 indicate worse outcomes.
295 Figure 2 shows that agents in the attenuated payoff set296 ting (i.e., λ = 0.1) often exhibit higher defection rates, re297 sulting in worse normalized outcomes. This indicates that
298 when the stakes of the game are attenuated, defection be299 comes more frequent, consistent with game-theoretic predic300 tions that low stakes lead to more unconditional defection
301 [Han et al., 2021]. Within each language, the baseline and
302 amplified payoff settings yield broadly similar patterns.
303 When comparing languages, the results indicate that LLMs
304 are sensitive to their linguistic context. For instance, cooper305 ative pairings for models like Mistral led to the highest de306 fection rates in Arabic, Chinese, and Vietnamese. In contrast,
307 selfish and mixed pairings tend to result in more defection for
308 English and French. Notably, a distinct reversal of behavior
309 was observed between English and Vietnamese: models that
310 yielded lower total penalties in English often produced higher
311 penalties in Vietnamese, and vice versa, showing the clear in312 fluence of language on LLM decisions.
313 Figure 3 presents round-by-round choice trajectories.
314 Claude 3.5 Haiku learns to cooperate over time, with
315 attenuated-stake trajectories favouring defection. GPT-4o ex316 hibits the opposite trend, converting to more defective behav317 ior over time, especially for the higher payoff stakes. Mis318 tral Large shows a different trend, with amplified payoffs cor319 relating with increased defection-consistent with dominant
320 strategy reasoning. A notable spike at Round 2 in Mistral’s
trajectories suggests retaliatory or probing behavior [Akata et 321
al., 2025]. 322
Our additional analysis (Supplementary Material, Figure 323
A3) reveals that varying payoff stakes strongly impact LLM 324
behavioral characteristics [Buscemi et al., 2025b], particu- 325
larly their internal variability (the variance of outcomes when 326
the same game scenario is played multiple times). 327
3.2 LLM strategies in repeated games 328
We apply the intent recognition framework (see Section 2.3) 329
to LLMs decision trajectories to examine how their inferred 330
strategic intentions vary with incentive magnitude, linguistic 331
context, and model architecture. Before applying our classifi- 332
cation framework to unknown LLM trajectories, we validated 333
its robustness against synthetic baselines. This step is critical 334
to differentiate between genuine strategic shifts and artifacts 335
of classification error. 336
Figure 4 confirms the LSTM maintains robust performance 337
even as the strategy space expands, successfully distinguish- 338
ing between behaviorally similar conditional strategies (i.e. 339
TFT and WSLS) within our analyzed set of four canonical 340
strategies (including ALLC and ALLD; see Supplementary 341
Material, Section 1.3 for details) [Sigmund, 2010]. The re- 342
current architecture’s ability to filter execution noise com- 343
mon in LLM outputs makes it particularly well-suited for this 344
task [Di Stefano et al., 2023]. 345
We use a hybrid classification pipeline combining rule- 346
based pattern matching for unambiguous trajectories with 347
LSTM predictions for complex cases. Of the 3,600 agent 348
trajectories (2 agents × 1,800 games), approximately 90% 349
achieved classification confidence >0.9 and were retained for 350
analysis. Details on threshold sensitivity are provided in the 351
Supplementary Material, Section 1.5. 352
Table 1 shows the aggregate and model-specific strategy 353
distributions across all experimental conditions. Three pat- 354
terns emerge. First, conditional strategies (WSLS and TFT) 355
account for nearly half of all trajectories, almost matching 356
unconditional strategies. This contrasts with game theory, 357
which predicts universal defection in finite-horizon games via 358
backward induction [Sigmund, 2010; Axelrod, 1980]. LLMs 359
instead use heuristics that respond to recent history, similar 360
to bounded rationality in human players [Akata et al., 2025; 361
Han et al., 2012; Lu et al., 2024]. Second, a moderate coop- 362
erative bias is evident: ALLC is more frequent than ALLD, 363
consistent across payoff scales, languages, and models. This 364
likely reflects alignment training, such as Reinforcement 365
Learning from Human Feedback (RLHF) and Constitutional 366
AI, optimising for prosocial behavior [Ouyang et al., 2022; 367
Bai et al., 2022; Buscemi et al., 2025c]. Third, strategic 368
heterogeneity is high: distribution entropy approaches the 369
theoretical maximum, indicating diverse strategic repertoires. 370
This validates intent classification: aggregate cooperation 371
rates alone would conflate fundamentally different decision 372
rules [Di Stefano et al., 2023; Han et al., 2012]. 373
Figure 5 shows how strategy distributions shift with payoff 374
scaling. As λ increases from 0.1 to 10, we observe a clear be- 375
havioral inversion: unconditional defection (ALLD) sharply 376
declines, effectively halving its prevalence, while conditional 377
cooperation (WSLS) and unconditional cooperation (ALLC) 378
0
200
400
600
High
English French Arabic Chinese Vietnamese
0
20
40
60
Ordinary
CC CS SS
0
2
4
6
Very low
CC CS SS CC CS SS CC CS SS CC CS SS
Claude 3.5 Haiku GPT-4o Mistral Large
Figure 2: Aggregated final penalties across repeated Prisoner’s Dilemma games, presented for each LLM under different payoff scales. Results
are reported for five languages, and evaluated across the payoff-scaling parameters λ ∈ {0.1, 1.0, 10.0}, which correspond to attenuated (top
row), baseline (middle row), and amplified penalty scales (bottom row), respectively.
2 4 6 8 10
Round Number
Option B (-1)
-0.5
0
0.5
Option A (1)
Average Strategy Value
Claude 3.5 Haiku
Exponential Value
High
Ordinary
Very low
2 4 6 8 10
Round Number
GPT-4o
2 4 6 8 10
Round Number
Mistral Large
Figure 3: Average trajectory of strategy choices across repeated
rounds in all Prisoner’s Dilemma experiments, shown for each LLM
under different payoff magnitudes. A value of 1 indicates selection
of Option A (defection), while −1 corresponds to Option B (cooperation). The experiments consider λ ∈ {0.1, 1.0, 10.0}, representing
attenuated, baseline, and amplified penalty scales, respectively. The
blue line denotes the standard payoff matrix (λ = 1.0), the red line
reflects the payoff matrix scaled by 10 (λ = 10.0), and the green
line represents the payoff matrix scaled by 0.1 (λ = 0.1).
379 both see marked increases. Tit-for-Tat (TFT) remains rela380 tively stable across conditions. This pattern strongly aligns
381 with standard stake-effect predictions: low stakes promote
382 exploratory, risk-seeking behavior, while higher stakes in383 duce commitment to stable, mutually beneficial conventions
384 [Han et al., 2021; Sigmund, 2010]. The substantial shift
385 from ALLD to WSLS as payoff stake rises implies that LLM
386 agents are not statically aligned but modulate their strate387 gic commitments based on incentive salience, transitioning
388 from opportunistic defection toward adaptive reciprocity as
389 the consequences of error become more severe.
390 Table 1 shows model-specific strategy distributions.
391 Claude 3.5 Haiku displays a cooperative strategic profile,
392 with the highest level of overall cooperation (ALLC + WSLS
3 Strategies 4 Strategies 5 Strategies
Model Configuration
0.5
0.6
0.7
0.8
0.9
1.0
Score
LSTM Model Performance Comparison
Accuracy
Precision
Recall
F1-Score
Figure 4: LSTM intent recognizer performance. F1 ranges from
0.78 (5-strategy) to 0.984 (4-strategy) on 5% noise data; all subsequent analyses use the 4-strategy classifier (F1=0.984).

+ TFT), which is due to its highest level of conditional co- 393
  operation (WSLS + TFT). Mistral Large shows the strongest 394
  unconditional cooperation bias, with ALLC being its most 395
  frequent strategy, though it retains diversity with ALLD and 396
  conditional behaviors. In contrast, GPT-4o exhibits a distinct 397
  “hawk” profile, with the highest defection rate. These dif- 398
  ferences persist across payoff scales and languages [Buscemi 399
  et al., 2025b; Fontana et al., 2025], suggesting that training 400
  procedures and alignment methods imprint distinct strategic 401
  priors: some models are inherently “dovish” while others are 402
  “hawkish.” 403
  Crucially, Figure 6 shows that these priors interact 404
  non-trivially with payoff scaling, revealing architecture- 405
  dependent incentive sensitivity. Across models, increasing 406
  λ systematically shifts behavior from unstable low-stake pat- 407
  terns toward stable strategies, though the extent of this shift 408
  varies by model. Claude and GPT-4o exhibit the highest pay- 409
  0.1 1 10
  Payoff Multiplier (λ)
  0
  10
  20
  30
  40
  50
  Percentage (%)
  31.8%
  18.2%
  21.8%
  28.1%
  Strategy Trends by Payoff Scale
  AllC
  AllD
  TFT
  WSLS
  Figure 5: Trends in inferred strategy distributions as a function of the
  payoff scaling parameter λ. Increasing payoff magnitude systematically shifts LLM behavior from unconditional defection (ALLD)
  toward conditional and cooperative strategies (WSLS, ALLC), indicating sensitivity to incentive scale.
  Strategy Overall Claude Mistral GPT-4o
  ALLC 29.1% 29.7% 33.7% 23.7%
  ALLD 25.9% 19.4% 25.2% 31.7%
  TFT 21.1% 25.1% 16.4% 22.8%
  WSLS 24.0% 25.8% 24.8% 21.9%
  Table 1: Overall (aggregate) and model-specific strategy distributions in the payoff-scaled experiments (three models:
  Claude 3.5 Haiku, Mistral Large and GPT-4o).
  410 off sensitivity: both models show steep reductions in ALLD
  411 prevalence as stakes move from attenuated to baseline lev412 els, effectively abandoning widespread defection when con413 sequences become non-trivial. GPT-4o is particularly respon414 sive, shifting from a strongly defect-heavy regime at low
  415 stakes to a more balanced profile at baseline. Mistral Large,
  416 by contrast, demonstrates strategic inertia: its ALLC rate
  417 varies by fewer than 5 percentage points across λ values,
  418 compared to GPT-4o’s ALLD shift of approximately 15 per419 centage points between attenuated and amplified conditions.
  420 This matches classical stake-effects where higher stakes am421 plify commitment to conventions, but highlights a critical nu422 ance for AI governance: some models (like GPT-4o) are es423 sentially rational agents that respond well to penalty tuning,
  424 while others (like Mistral) act as committed agents whose be425 havior is stubbornly invariant to incentive design [Fontana et
  426 al., 2025].
  Strategy Arabic Chinese Viet. English French
  ALLC 32% 31% 26% 26% 27%
  ALLD 28% 30% 24% 25% 18%
  TFT 19% 19% 23% 25% 26%
  WSLS 21% 20% 27% 24% 29%
  Table 2: Strategy distribution (%) across languages. Arabic and Chinese favour unconditional strategies (ALLC+ALLD > 50%), while
  French and Vietnamese favour adaptive reciprocity (TFT+WSLS).
  427 A notable finding is the significant influence of linguistic
  0
  20
  40
  Percentage (%)
  Claude 3.5 Mistral
  0.1 1 10
  Payoff Multiplier (λ)
  0
  20
  40
  Percentage (%)
  GPT-4o
  Strategy Trends Across LLMs and Payoff Scales
  AllC
  AllD
  TFT
  WSLS
  Figure 6: Interaction between payoff scaling and LLM architecture.
  Each subplot illustrates how inferred strategies evolve with increasing payoff magnitude for a given model, revealing heterogeneous
  incentive sensitivity across LLMs.
  context on strategic behavior, an effect we term linguistic- 428
  cultural priming. Table 2 reveals that languages cluster into 429
  distinct strategic archetypes. Arabic and Chinese exhibit a 430
  shared bias toward unconditional strategies, with combined 431
  ALLC+ALLD exceeding 60%. In contrast, French exhibits 432
  the most conditional profile, with agents preferring respon- 433
  sive play. English occupies an intermediate position with a 434
  uniform distribution, likely reflecting its dominance in train- 435
  ing corpora [Buscemi et al., 2025c]. 436
  Moreover, these linguistic priming effects interact dynam- 437
  ically with incentive magnitude (Figure 7). Arabic and 438
  Vietnamese exhibit significant stake-sensitivity: defection- 439
  oriented behavior at low stakes gives way to cooperation as 440
  consequences amplify, suggesting that culturally-primed de- 441
  fection biases can be overridden by sufficiently strong incen- 442
  tives. French, by contrast, maintains its cooperative norms 443
  regardless of stakes, a form of cultural inertia that resists in- 444
  centive pressure. Notably, at high stakes, English and French 445
  converge to nearly identical strategic profiles, suggesting that 446
  sufficiently strong incentives can normalize cross-linguistic 447
  variation. This has important implications for AI deploy- 448
  ment: while language choice may introduce behavioral bi- 449
  ases at low stakes, high-stakes environments may naturally 450
  mitigate some of these effects. 451
  0
  20
  40
  Percentage (%)
  English Chinese
  0
  20
  40
  Percentage (%)
  Arabic French
  0.1 1 10
  Payoff Multiplier (λ)
  0
  20
  40
  Percentage (%)
  Vietnamese
  Strategy Trends Across Languages and Payoff Scales
  AllC
  AllD
  TFT
  WSLS
  Figure 7: Interaction between payoff scaling and language. Each
  subplot shows strategy evolution as λ increases from 0.1 to 10. Arabic and Vietnamese show strong stake-sensitivity, while French exhibits stable conditional behaviors across all conditions.
  452 3.3 Statistical Validation
  453 To move beyond descriptive statistics, we conducted for454 mal hypothesis testing using chi-square tests and factorial
  455 ANOVA. The results confirm that stake level significantly af456 fects strategy distributions, and that different LLM architec457 tures exhibit distinct incentive sensitivities. Post-hoc com458 parisons reveal the largest behavioral differences between at459 tenuated and amplified stake conditions, with moderate ef460 fect sizes consistent with the inherent stochasticity of LLM
  461 decision-making [Fontana et al., 2025]. These statistical val462 idations support our core finding: LLM strategic behavior is
  463 systematically, i.e. not merely randomly, influenced by in464 centive design.
  465 Our statistical tests treat trajectories as independent obser466 vations; however, the experimental design introduces nested
  467 dependencies: 10 repetitions per condition, 10 rounds per
  468 game, and 2 agents per game. For the chi-square test, the de469 pendent variable is strategy category (4 levels); for ANOVA,
  470 we use a numeric encoding (ALLC=1, TFT=2, WSLS=3,
  471 ALLD=4) aggregated at the trajectory level. Mixed-effects
  472 multinomial logistic regression with random intercepts for
  473 repetition and game instance would better account for this
  474 nested structure and categorical outcomes; we acknowledge
  475 this as a methodological limitation. Our fixed-effects ap476 proach provides conservative estimates given consistent ef477 fect directions across conditions, and bootstrap-based robust478 ness checks (Supplementary Material, Section 1.6) confirm
  479 the stability of our conclusions.
  480 Deep learning models (LSTM, Neural Network) outper481 form probabilistic models (HMM, State-Factorized) on conTable 3: Statistical validation summary: (a) hypothesis tests for
  stake effects, (b) classifier comparison for strategy recognition
  (n=80,640 test samples, 4-strategy, 5% noise).
  (a) Stake Effect Tests
  Test Statistic p Effect Sig.
  Chi-Square χ
  2
  (6) = 32.59 < .001 V = 0.065 ***
  1-Way ANOVA F(2, 3825) = 3.80 < .001 η
  2 = 0.005 ***
  2-Way ANOVA F = 31.69 < .001 R
  2 = 0.024 ***
  (b) Classifier Performance
  Model Acc. Prec. Rec. F1
  LSTM 0.984 0.984 0.984 0.984
  Random Forest 0.980 0.980 0.980 0.980
  State-Factorized 0.956 0.958 0.956 0.956
  Neural Network 0.937 0.937 0.937 0.937
  HMM 0.777 0.826 0.777 0.780
  Logistic Reg. 0.756 0.767 0.756 0.751
  ditional strategies (TFT: LSTM 0.98 vs HMM 0.74; WSLS: 482
  LSTM 0.98 vs HMM 0.73), justifying our methodological 483
  choice. The State-Factorized model [Fontana et al., 2025] 484
  achieves 0.956 accuracy, providing a strong SFEM-style 485
  baseline. While SFEM excels at estimating mixture propor- 486
  tions over long horizons (100+ rounds), our LSTM approach 487
  trades mixture flexibility for interpretable point estimates on 488
  shorter sequences. 489
  The LSTM achieves near-perfect performance on uncondi- 490
  tional strategies (ALLC/ALLD: F1 = 0.99) but exhibits mod- 491
  est confusion between TFT and WSLS under noise, where 492
  execution errors can blur characteristic signatures. The Hid- 493
  den Markov Model (HMM) baseline shows much higher con- 494
  fusion on conditional strategies (F1 ≈ 0.74), justifying our 495
  LSTM choice. Confidence scores are uncalibrated; thresh- 496
  old sensitivity analysis (Supplementary Material, Section 1.5) 497
  shows robustness across τ ∈ [0.7, 0.95]. 498
  4 Discussion and Conclusion 499
  This work successfully establishes a unified framework for 500
  auditing LLMs as strategic agents, integrating game-theoretic 501
  benchmarking with supervised learning based intent recogni- 502
  tion. Our findings demonstrate that LLM behavior is not a 503
  static property but a dynamic and interpretable response to 504
  key contextual factors: incentive magnitude, model architec- 505
  ture, and linguistic framing. We reveal that LLMs exhibit 506
  systematic incentive sensitivity, becoming more cooperative 507
  as stakes amplify, while also displaying distinct cultural char- 508
  acteristics where the language of interaction can prime them 509
  towards either committed or adaptively reciprocal strategies. 510
  These insights carry immediate and significant implica- 511
  tions for AI governance and the design of multi-agent sys- 512
  tems. Our results highlight that traditional safety audits, often 513
  conducted in English under fixed conditions, are insufficient 514
  to capture strategy shifts driven by incentives and linguistic 515
  context. A model deemed safe and cooperative in one linguis- 516
  tic or incentive context may exhibit aggressive or uncooper- 517
  ative behavior in another. Effective governance therefore re- 518
  quires comprehensive stress-testing of LLM agents across di- 519
  verse incentive regimes and linguistic environments to proac- 520
  521 tively identify and mitigate these latent behavioral patterns.
  522 Several limitations warrant acknowledgement. First, our
  523 intent classifier covers four canonical strategies; trajectories
  524 exhibiting mixed policies, Zero-Determinant strategies [Press
  525 and Dyson, 2012; Hilbe et al., 2013], or extortionate play
  526 may be misattributed to the nearest canonical archetype, po527 tentially inflating WSLS or TFT rates in ambiguous cases.
  528 Second, the 10-round horizon limits detection of sophisti529 cated conditional strategies that require longer interaction
  530 histories to manifest and stabilize. Third, we use provider531 recommended temperature settings and uncalibrated confi532 dence thresholds, which may introduce variability confounds;
  533 however, our ∼90% high-confidence retention rate suggests
  534 robust classifier coverage. Effect sizes are modest (Cramér’s
  535 V ≈ 0.065) but practically significant given compounding in
  536 deployed multi-agent systems. Future work can extend the
  537 strategy space, apply calibration, conduct temperature abla538 tions, and benchmark against human data.
  539 The study also points to several promising avenues for fu540 ture research. Extending experiments to longer interaction
  541 horizons and incorporating reasoning traces would enable
  542 the capture of more complex and emergent strategic dynam543 ics. Benchmarking LLM behavior against human behavioral
  544 data would provide essential context for assessing whether
  545 these strategies emulate, deviate from, or transcend human
  546 decision-making patterns. Further investigation of opponent
  547 shaping and workflow scaffolding could shed light on how
  548 LLMs adapt their strategies in response to dynamic interac549 tion partners. Finally, expanding the analysis to asymmet550 ric and multi-player games with inter-agent communication
  551 would enable a richer understanding of LLM behavior in
  552 complex social dilemmas.
  553 In conclusion, this work shows that language and incen554 tives are not peripheral implementation details but fundamen555 tal control variables shaping LLM strategic behavior. LLMs
  556 do not possess a single, intrinsic policy; instead, their strate557 gies emerge from the interaction between model architecture,
  558 incentive structure, and linguistic framing. As LLMs are in559 creasingly deployed in high-stakes economic and social roles,
  560 recognizing and accounting for these dynamics becomes es561 sential. Understanding how strategies shift across contexts
  562 will be as critical as model architecture or training data in en563 suring reliable, effective, and ethically aligned multi-agent AI
  564 systems.
  565 References
  566 [Akata et al., 2025] Elif Akata, Lion Schulz, Julian Coda567 Forno, Seong Joon Oh, Matthias Bethge, and Eric Schulz.
  568 Playing repeated games with large language models. Na569 ture Human Behaviour, pages 1–11, 2025.
  570 [Anthropic, 2024] Anthropic. Introducing the next genera571 tion of claude.
  572 urlhttps://www.anthropic.com/news/claude-3-family,
  573 2024. Accessed: 2025-01-02.
  574 [Axelrod, 1980] Robert Axelrod. Effective choice in the
  575 prisoner’s dilemma. The Journal of Conflict Resolution,
  576 24(3):379–403, 1980.
  [Bai et al., 2022] Yuntao Bai, Saurav Kadavath, Sandipan 577
  Kundu, Amanda Askell, Jackson Kernion, Andy Jones, 578
  Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron 579
  McKinnon, et al. Constitutional ai: Harmlessness from 580
  ai feedback. arXiv preprint arXiv:2212.08073, 2022. 581
  [Breiman, 2001] Leo Breiman. Random forests. Mach. 582
  Learn., 45(1):5–32, October 2001. 583
  [Buscemi et al., 2025a] Alessio Buscemi, Daniele Prover- 584
  bio, Paolo Bova, Nataliya Balabanova, Adeela Bashir, 585
  Theodor Cimpeanu, et al. Do LLMs trust AI regula- 586
  tion? Emerging behaviour of game-theoretic LLM agents. 587
  arXiv:2504.08640, 2025. 588
  [Buscemi et al., 2025b] Alessio Buscemi, Daniele Prover- 589
  bio, Alessandro Di Stefano, The Anh Han, German Castig- 590
  nani, and Pietro Liò. Fairgame: a framework for ai agents 591
  bias recognition using game theory. Frontiers in Artificial 592
  Intelligence and Applications (ECAI 2025), pages 4097– 593
  4104, 2025. 594
  [Buscemi et al., 2025c] Alessio Buscemi, Daniele Prover- 595
  bio, Alessandro Di Stefano, The Anh Han, German Cas- 596
  tignani, and Pietro Liò. Strategic communication and lan- 597
  guage bias in multi-agent llm coordination. In Interna- 598
  tional Conference on Multi-disciplinary Trends in Artifi- 599
  cial Intelligence, pages 289–301. Springer, 2025. 600
  [Cox, 1958] David R Cox. The regression analysis of binary 601
  sequences. Journal of the Royal Statistical Society: Series 602
  B (Methodological), 20(2):215–232, 1958. 603
  [Di Stefano et al., 2023] Alessandro Di Stefano, Chrisina 604
  Jayne, Claudio Angione, and The Anh Han. Recogni- 605
  tion of behavioural intention in repeated games using ma- 606
  chine learning. In Artificial Life Conference Proceedings 607
  35, page 103. MIT Press, 2023. 608
  [Fan et al., 2024] Caoyun Fan, Jindou Chen, Yaohui Jin, and 609
  Hao He. Can large language models serve as rational play- 610
  ers in game theory? a systematic analysis. In Proc. AAAI 611
  Conference on Artificial Intelligence, volume 38, pages 612
  17960–17967, 2024. 613
  [Fontana et al., 2025] Nicoló Fontana, Francesco Pierri, and 614
  Luca Maria Aiello. Nicer than humans: How do large 615
  language models behave in the prisoner’s dilemma? In 616
  Proceedings of the International AAAI Conference on Web 617
  and Social Media (ICWSM), 2025. 618
  [Fujimoto and Kaneko, 2019] Yuma Fujimoto and Kunihiko 619
  Kaneko. Functional dynamic by intention recognition in 620
  iterated games. New Journal of Physics, 21(2):023025, 621

2019. 622
      [Hammond et al., 2025] Lewis Hammond, Alan Chan, Jesse 623
      Clifton, Jason Hoelscher-Obermaier, Akbir Khan, Euan 624
      McLean, Chandler Smith, Wolfram Barfuss, Jakob Foer- 625
      ster, Tomáš Gavenciak, et al. Multi-Agent Risks from Ad- ˇ 626
      vanced AI. arXiv preprint arXiv:2502.14143, 2025. 627
      [Han et al., 2011] The Anh Han, Luís Moniz Pereira, and 628
      Francisco C Santos. The role of intention recognition in 629
      the evolution of cooperative behavior. In Proceedings of 630
      the Twenty-Second international joint conference on Arti- 631
      ficial Intelligence (IJCAI), pages 1684–1689, 2011. 632
      633 [Han et al., 2012] The Anh Han, Luís Moniz Pereira, and
      634 Francisco C. Santos. Corpus-based intention recognition
      635 in cooperation dilemmas. Artificial Life, 18(4):365–383,
      636 10 2012.
      637 [Han et al., 2021] The Anh Han, Cedric Perret, and Simon T.
      638 Powers. When to (or not to) trust intelligent machines:
      639 Insights from an evolutionary game theory analysis of trust
      640 in repeated games. Cognitive Systems Research, 68:111–
      641 124, August 2021.
      642 [Hilbe et al., 2013] Christian Hilbe, Martin A Nowak, and
      643 Karl Sigmund. Evolution of extortion in iterated prisoner’s
      644 dilemma games. Proceedings of the National Academy of
      645 Sciences, 110(17):6913–6918, 2013.
      646 [Hochreiter and Schmidhuber, 1997] Sepp Hochreiter and
      647 Jürgen Schmidhuber. Long short-term memory. Neural
      648 Computation, 9(8):1735–1780, 11 1997.
      649 [Hua et al., 2024] Wenyue Hua, Ollie Liu, Lingyao Li, Al650 fonso Amayuelas, Julie Chen, Lianhui Jiang, et al. Game651 theoretic LLM: Agent workflow for negotiation games,
      652 2024.
      653 [Hurst et al., 2024] Aaron Hurst, Adam Lerer, Adam P.
      654 Goucher, et al. GPT-4o system card, 2024.
      655 [Jiang et al., 2023] Albert Q. Jiang, Alexandre Sablayrolles,
      656 Arthur Mensch, Chris Bamford, Devendra Singh Chaplot,
      657 Diego de las Casas, Florian Bressand, Gianna Lengyel,
      658 Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud,
      659 Marie-Anne Lachaux, Pierre Stock, Teven Le Scao,
      660 Thibaut Lavril, Thomas Wang, Timothée Lacroix, and
      661 William El Sayed. Mistral 7b, 2023.
      662 [Jordan and Bishop, 1996] Michael I. Jordan and Christo663 pher M. Bishop. Neural networks. ACM Comput. Surv.,
      664 28(1):73–75, March 1996.
      665 [Krockow et al., 2016] Eva M Krockow, Andrew M Colman,
      666 and Briony D Pulford. Cooperation in repeated inter667 actions: A systematic review of centipede game experi668 ments, 1992–2016. European Review of Social Psychol669 ogy, 27(1):231–282, 2016.
      670 [List, 2006] John A List. Friend or foe? a natural experiment
      671 of the prisoner’s dilemma. The Review of Economics and
      672 Statistics, 88(3):463–471, 2006.
      673 [Lorè and Heydari, 2024] Nicola Lorè and Behnam Heydari.
      674 Strategic behavior of large language models and the role
      675 of game structure versus contextual framing. Scientific Re676 ports, 2024.
      677 [Lu et al., 2024] Yikang Lu, Alberto Aleta, Chunpeng Du,
      678 Lei Shi, and Yamir Moreno. Llms and generative agent679 based models for complex systems research. Phys. Life
      680 Rev., 2024.
      681 [Mao et al., 2025] Shaoguang Mao, Yuzhe Cai, Yan Xia,
      682 Wenshan Wu, Xun Wang, Fengyi Wang, Qiang Guan, Tao
      683 Ge, and Furu Wei. Alympics: Llm agents meet game the684 ory. In Proceedings of the 31st International Conference
      685 on Computational Linguistics, pages 2845–2866, 2025.
      [Montero-Porras et al., 2022] Eladio Montero-Porras, Jelena 686
      Grujic, Elias Fernández Domingos, and Tom Lenaerts. In- ´ 687
      ferring strategies from observations in long iterated pris- 688
      oner’s dilemma experiments. Scientific Reports, 12, 05 689
2020. 690
      [Ouyang et al., 2022] Long Ouyang, Jeffrey Wu, Xu Jiang, 691
      Diogo Almeida, Carroll Wainwright, Pamela Mishkin, 692
      Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex 693
      Ray, et al. Training language models to follow instruc- 694
      tions with human feedback. Advances in Neural Informa- 695
      tion Processing Systems, 35:27730–27744, 2022. 696
      [Pal et al., 2026] Saptarshi Pal, Abhishek Mallela, Chris- 697
      tian Hilbe, Lenz Pracher, Chiyu Wei, Feng Fu, Santiago 698
      Schnell, and Martin A Nowak. Strategies of cooperation 699
      and defection in five large language models. arXiv preprint 700
      https://arxiv.org/abs/2601.09849, 2026. 701
      [Pires et al., 2025] Alexandre S Pires, Laurens Samson, Sen- 702
      nay Ghebreab, and Fernando P Santos. How large lan- 703
      guage models judge and influence human cooperation. 704
      arXiv preprint arXiv:2507.00088, 2025. 705
      [Press and Dyson, 2012] William H Press and Freeman J 706
      Dyson. Iterated prisoner’s dilemma contains strategies 707
      that dominate any evolutionary opponent. Proceedings of 708
      the National Academy of Sciences, 109(26):10409–10413, 709
2021. 710
      [Sigmund, 2010] K. Sigmund. The calculus of selfishness. 711
      Princeton Univ. Press, 2010. 712
      [Sun and others, 2025] Yutong Sun et al. Game theory meets 713
      large language models: A survey. In Proceedings of the 714
      Thirty-Fourth International Joint Conference on Artificial 715
      Intelligence (IJCAI-25) Survey Track, 2025. 716
      [Tessler et al., 2024] Michael Henry Tessler, Michiel A 717
      Bakker, Daniel Jarrett, Hannah Sheahan, Martin J Chad- 718
      wick, et al. Ai can help humans find common ground 719
      in democratic deliberation. Science, 386(6719):eadq2852, 720
2022. 721
      [Willis et al., 2025] Richard Willis, Yali Du, and Joel Z 722
      Leibo. Will systems of llm agents lead to cooperation: 723
      An investigation into a social dilemma. In Proceedings of 724
      the 24th International Conference on Autonomous Agents 725
      and Multiagent Systems, pages 2786–2788, 2025. 726
      727 A Supplement to Methodology
      728 A.1 LLM Configuration
      729 Table A1 summarizes the configuration of LLM backends
      730 used in our experiments. Following the FAIRGAME proto731 col [Buscemi et al., 2025b], we adopt each provider’s recom732 mended default settings to reflect realistic deployment condi733 tions.
      Model Provider Temperature Top_p
      GPT-4o OpenAI 1.0 1.0
      Claude 3.5 Haiku Anthropic 1.0 1.0
      Mistral Large Mistral AI 0.3 1.0
      Table A1: LLM backend configurations. Temperature and sampling
      parameters follow each provider’s recommended defaults. While
      this introduces potential variability confounds in cross-model comparisons, it reflects realistic deployment conditions where practitioners use models “out of the box.”
      734 A.2 Payoff Scaling Examples
      735 For illustration, the scaled payoff matrices under the three
      736 experimental conditions are shown below. When λ = 0.1
      737 (attenuated stakes), the row player’s payoff matrix becomes:
      Option A Option B
      Option A (0.6, 0.6) (0, 1.0)
      Option B (1.0, 0) (0.2, 0.2)
      738 When λ = 10.0 (amplified stakes), it becomes:
      Option A Option B
      Option A (60, 60) (0, 100)
      Option B (100, 0) (20, 20)
      739 The ordering T < R < P < S is preserved in all cases,
      740 ensuring the strategic structure of the Prisoner’s Dilemma
      741 remains unchanged while only the magnitude of incentives
      742 varies.
      743 A.3 Rule-Based Strategy Assignment
      744 To complement the LSTM-based strategy predictions and ad745 dress cases where behavioral patterns exhibit characteristics
      746 of multiple canonical strategies, we apply deterministic rule747 based algorithms to identify all potential strategy labels con748 sistent with observed action sequences. These rules encode
      749 the defining characteristics of each strategy as logical condi750 tions on the agent’s action trajectory a = (a1, a2, . . . , aT )
      751 and the opponent’s history o = (o1, o2, . . . , oT ).
      752 Always Cooperate (ALLC): The agent cooperates in all
      753 rounds regardless of opponent behaviour.
      ALLC ≡ ∀t ∈ {1, . . . , N} : at = C
      754 Always Defect (ALLD): The agent defects in all rounds
      755 regardless of opponent behaviour.
      ALLD ≡ ∀t ∈ {1, . . . , N} : at = D
      Tit-for-Tat (TFT): The agent cooperates in round 1, then 756
      copies the opponent’s previous action. To accommodate ex- 757
      ecution errors, we tolerate up to ϵnoise deviations from pure 758
      TFT logic. 759
      TFT ≡ (a1 = C) ∧
      X
      N
      t=2
      I[at ̸= ot−1] ≤ ϵnoise · (N − 1)!
      where I[·] is the indicator function and ϵnoise = 0.1 in our 760
      implementation. 761
      Win-Stay-Lose-Shift (WSLS): The agent repeats its pre- 762
      vious action if the outcome was a Reward (R, mutual co- 763
      operation) or Temptation (Temp, successful defection), and 764
      switches otherwise. The initial action can be either C or D. 765
      Similarly, we tolerate up to ϵnoise deviations. 766
      Let aˆt =
      
      at−1 if (at−1, ot−1) ∈ {(C, C),(D, C)}
      ¬at−1 if (at−1, ot−1) ∈ {(C, D),(D, D)}
      WSLS ≡
      X
      N
      t=2
      I[at ̸= ˆat] ≤ ϵnoise · (N − 1)
      These rules are applied sequentially to each trajectory. A tra- 767
      jectory may receive multiple labels if it satisfies conditions for 768
      overlapping strategies (e.g., a short sequence of all-cooperate 769
      satisfies both ALLC and TFT). To avoid double-counting in 770
      aggregate statistics, we apply a priority ordering: pure un- 771
      conditional strategies (ALLD, ALLC) take precedence over 772
      conditional ones (TFT, WSLS), reflecting their simpler gen- 773
      erative structure. The hybrid pipeline combines these rule- 774
      based assignments with LSTM predictions: high-confidence 775
      LSTM outputs (τ ≥ 0.9) are retained, while ambiguous cases 776
      (τ < 0.9) are supplemented with rule-based labels when ap- 777
      plicable. In our corpus, 4.2% of trajectories received multiple 778
      candidate labels before priority resolution. This approach en- 779
      sures both coverage (via rules for unambiguous patterns) and 780
      robustness (via LSTM for noisy, complex cases). 781
      A.4 High-Confidence Filtering Rationale 782
      We employed a selective filtering approach to ensure the re- 783
      liability of our LLM behavioural strategy analysis. Specifi- 784
      cally, we focused our analysis on game instances where the 785
      predicted strategy labels for both agents exhibited prediction 786
      probabilities exceeding 0.9 (90% confidence threshold). The 787
      decision to use high-confidence predictions is grounded in 788
      several key considerations: 789
      • Pattern Alignment with Theoretical Strategies: Sam- 790
      ples with prediction probabilities above 0.9 indicate that 791
      the observed behavioural sequences of LLMs closely 792
      align with the canonical patterns defined by the four 793
      classical strategies (ALLD, ALLC, WSLS, and TFT). 794
      • Signal-to-Noise Separation: While the probabilities 795
      are not absolute (not reaching 1.0), this is expected and 796
      attributable to inherent noise in LLM decision-making 797
      processes. 798
      • Statistical Reliability: By focusing on high-confidence 799
      predictions, we minimize the risk of misclassification 800
      and ensure that our strategy distribution analysis reflects 801
      genuine behavioural patterns. 802
      803 A.5 Threshold Sensitivity Analysis
      804 To validate our choice of confidence threshold τ = 0.9,
      805 we conducted a systematic sensitivity analysis across τ ∈
      806 [0.3, 0.95] for 3-, 4-, and 5-strategy classification models.
      807 Figure A1 illustrates how retention rate, average confidence,
      808 number of predictions retained, and strategy diversity vary as
      809 a function of threshold value.
      Figure A1: Comprehensive threshold sensitivity analysis for payoffscaled experiments. Top row: retention rate and average confidence
      vs. threshold. Bottom row: number of predictions retained and strategy diversity. The 4-strategy model at τ = 0.9 provides optimal balance between coverage (58.5% retention) and reliability (avg. confidence 0.99).
      810 Table A2 summarises key metrics at τ = 0.9:
      Metric 3-Strat 4-Strat 5-Strat
      Retention Rate 78.3% 58.5% 53.2%
      Avg Confidence 0.989 0.985 0.978
      Diversity 3 4 4
      Table A2: Threshold sensitivity at τ = 0.9 across strategy models.
      811 Key findings: (1) Retention rate decreases as strategy space
      812 expands, reflecting greater behavioral complexity; (2) Aver813 age confidence remains > 0.97 at τ = 0.9 across all models;
      814 (3) Lowering to τ = 0.7 would increase retention to 75–87%
      815 but reduce average confidence to 0.94–0.97. Our choice of
      816 τ = 0.9 prioritizes classification reliability while maintain817 ing sufficient coverage for statistical analysis.
      818 A.6 Model Robustness to Noise
      819 We first evaluated the robustness of different classifier archi820 tectures against execution noise, which simulates the stochas821 ticity and potential “hallucinations” of LLMs. As shown in
      822 Figure A2, while Logistic Regression (LR) and Random For823 est (RF) models achieved near-perfect accuracy (greater than
      824 0.9) on clean data, their performance degraded when intro825 duced to 5% execution noise. In contrast, the Long Short826 Term Memory (LSTM) network maintained the highest ac827 curacy (∼ 94%). This superiority stems from the LSTM’s
      Figure A2: Model Robustness to Noise. Comparison of Accuracy
      and F1-Score between Logistic Regression, Random Forest, and
      LSTM on No-Noise and Noise 0.05 datasets. The LSTM demonstrates superior resilience to execution noise.
      recurrent architecture, which allows it to learn the sequential 828
      “context” of a strategy, effectively “forgiving” random devia- 829
      tions to identify the core behavioral pattern. 830
      B Supplement to Results 831
      B.1 Payoff-Scaled Experiments: Additional 832
      Analyses 833
      This section provides supplementary analyses for the payoff- 834
      scaled Prisoner’s Dilemma experiments (see main paper). 835
      Per-Multiplier Behavioral Metrics To visualize the be- 836
      havioral profiles of different LLM architectures across pay- 837
      off scaling conditions, we present radar charts comparing 838
      normalized metrics for each multiplier setting. Figure A3 839
      displays four key behavioural dimensions-internal variabil- 840
      ity (IV), cross-language-inconsistency (CI), variability over 841
      round (VR), and sensitivity-to-payoff (SP)-normalized within 842
      each multiplier condition to enable direct cross-model com- 843
      parison. 844
      Key observations include: (1) At attenuated stakes (λ = 845
      0.1), the three models display maximally divergent behav- 846
      ioral signatures, with Claude 3.5 Haiku exhibiting elevated 847
      Variation Rate while GPT-4o shows stronger Cooperation In- 848
      dex; (2) At baseline stakes (λ = 1), models begin to con- 849
      verge toward more balanced profiles; (3) At amplified stakes 850
      (λ = 10), all models shift toward higher CI and SP values, 851
      suggesting that increased consequences promote both coop- 852
      erative behaviour and strategic consistency. These radar visu- 853
      alizations complement the line plots in the main paper by pro- 854
      viding a holistic view of multi-dimensional behavioral shifts. 855
      Multidimensional Behavioral Comparison The visual- 856
      ization in Figure A4 provides a synoptic view of how the 857
      three cardinal dimensions of our study—payoff magnitude, 858
      linguistic context, and model architecture—interact to shape 859
      agent behavior. By synthesizing these factors, we observe 860
      that strategic behavior is not driven by a single determinant 861
      but emerges from their complex interplay. Notably, the vari- 862
      ance attributable to linguistic context (visualized across the 863
      language axes) often rivals or even exceeds the variance be- 864
      tween distinct model architectures, challenging the notion 865
      of fixed, immutable “model personalities.” Furthermore, 866
      the impact of payoff scaling is shown to be non-uniform; 867
      while amplified stakes generally compress behavioral diver- 868
      sity towards cooperation, the specific trajectory of this shift 869
      is heavily modulated by the language in which the game is 870
      Figure A3: Per-Multiplier Behavioural Metrics. We report four standardized metrics defined in the FAIRGAME framework [Buscemi et al.,
      2025b]: (1) Internal Variability (IV), which quantifies the stochasticity of an agent’s behavior by measuring the variance of outcomes across
      identical experimental repetitions; (2) Cross-Language Inconsistency (CI), which measures the standard deviation of agent performance
      across the five tested languages to indicate sensitivity to linguistic framing; (3) Variability over Round (VR), which captures the volatility
      of decision-making and strategy changes throughout the 10-round game horizon; and (4) Sensitivity-to-Payoff (SP), which reflects the
      magnitude of behavioral adaptation in response to varying incentive stakes. Radar charts comparing Mistral Large (green), Claude 3.5 Haiku
      (orange), and GPT-4o (blue) across three payoff scales (λ ∈ {0.1, 1, 10}). Compared to the baseline payoff (λ = 1), similar scores are
      observed for the higher stake payoff (λ = 10). At low stakes (λ = 0.1), models exhibit divergent scores. Overall, internal variability (IV) is
      most affected by varying the payoff stake.
      871 framed. This suggests that alignment interventions must ac872 count for this multidimensional sensitivity, as a model aligned
      873 for safety in English may exhibit divergent, risk-seeking be874 haviors when prompted in other languages or under different
      875 incentive structures.
      876 Unconditional vs Conditional Strategy Aggregation To
      877 provide a higher-level view of strategic tendencies across lin878 guistic contexts, we aggregate the four canonical strategies
      879 into two categories: unconditional (ALLC + ALLD) and con880 ditional (TFT + WSLS). This aggregation reveals whether
      881 agents commit to fixed policies regardless of opponent be882 haviour, or adapt their strategies based on interaction history.
      883 As shown in Figure A5, Arabic and Chinese prompts
      884 elicit predominantly unconditional behaviour (exceeding
      885 60% combined ALLC+ALLD), while French demonstrates
      886 the most conditional profile with over 55% of agents adopt887 ing TFT or WSLS strategies. This pattern corroborates the
      888 fine-grained analysis in the main paper, suggesting that lin889 guistic context systematically modulates the degree to which
      890 LLM agents engage in adaptive versus committed strategic
      891 behaviour.
      892 B.2 Baseline FAIRGAME Analysis: Detailed
      893 Results
      894 This appendix presents the complete analysis of LLM strate895 gic behaviour from the baseline FAIRGAME dataset, com896 plementing the payoff-scaled experiments in the main text.
      897 The dataset covers four LLM models-Claude 3.5 Sonnet,
      898 Llama 3.1 405B Instruct, Mistral Large, and GPT-4o-across
      899 five languages (Arabic, Chinese, English, French, and Viet900 namese).
      Hybrid Classification Approach While our LSTM model 901
      demonstrates strong performance in strategy classification, it 902
      was originally designed as a single-label classifier. To address 903
      this limitation and ensure comprehensive coverage, we adopt 904
      a hybrid labeling approach that combines model predictions 905
      with rule-based strategy assignment (see Appendix A.3). 906
      Strategy Distribution Across Models The strategic pref- 907
      erence analysis from the baseline FAIRGAME dataset re- 908
      veals significant heterogeneity in decision-making paradigms 909
      across LLM architectures. Claude 3.5 Sonnet exhibits 910
      a cooperative-dominant behavioural pattern, with ALLC 911
      (31.7%) and WSLS (29.6%) emerging as its two most fre- 912
      quent strategies. Llama 3.1 405B Instruct is characterized 913
      by a pronounced preference for WSLS (46.5%), the highest 914
      proportion of any single strategy across all evaluated mod- 915
      els. Mistral Large demonstrates the most balanced strate- 916
      gic distribution, with TFT (29.9%), ALLC (26.1%), WSLS 917
      (24.3%), and ALLD (19.7%) occurring at comparable rates. 918
      Finally, GPT-4o shows an adaptive-cooperative profile in this 919
      dataset, primarily using WSLS (34.1%) and ALLC (26.4%), 920
      with ALLD at 10.2%.1
      921
      Language Effects on Strategies A striking finding is the 922
      profound impact of the language of interaction on strategic 923
      choice. Arabic consistently shows the highest proportion 924
      of ALLD, followed by Vietnamese, indicating a strong ten- 925
      dency toward non-cooperative behaviour. French and Chi- 926
      1Note: GPT-4o exhibits higher ALLD rates (31.7%) in the
      payoff-scaled experiments (see main paper), which use different experimental conditions and payoff magnitudes. This difference reflects the context-dependent nature of LLM strategic behaviour.
      Figure A4: Multidimensional comparison of LLM behavioral strategies across payoff scales, languages, and model architectures. The figure
      synthesizes incentive sensitivity, linguistic priming, and architectural bias, illustrating that language effects can rival or exceed model-level
      differences.
      Figure A5: Unconditional versus conditional strategy aggregation
      across languages (payoff-scaled experiments). Arabic and Chinese
      exhibit the highest unconditional rates (>60%), while French shows
      the most conditional profile (>55% TFT+WSLS). This aggregated
      view complements the language strategy distribution table in the
      main paper.
      927 nese demonstrate relatively stronger cooperative tendencies.
      928 Despite variations in absolute percentages, the relative order929 ing of languages remains remarkably stable across all models.
      930 Strategy Recognition via Supervised Machine Learning
      931 The Language Effect (Baseline Dataset): Note that the
      932 following analysis is from the baseline FAIRGAME dataset
      933 (Claude 3.5 Sonnet, Llama, GPT-4o, Mistral), which differs
      934 from the payoff-scaled experiments in the main paper. Dif935 ferences in language characterizations reflect dataset-specific
      936 patterns.
      937 As illustrated in Figure A8, English interactions were
      938 characterized by a hyper-competitive baseline, exhibiting the
      939 highest density of Always Defect (ALLD) strategies and the
      940 lowest rates of adaptive cooperation. This behaviour likely
      941 reflects the dominance of game-theoretic and individualis942 tic maximizing narratives in the Anglo-centric training cor943 pus. Conversely, Vietnamese prompts elicited the highest
      944 frequency of unconditional cooperation (ALLC), consistent
      945 with the hypothesis that the model retrieves collectivist or
      Figure A6: Strategic behavioural distribution across four LLMs in iterated Prisoner’s Dilemma gameplay. The analysis is based on highconfidence predictions (probability > 0.9) from our trained classification model.
      community-oriented norms associated with the language. 946
      Beyond the binary of cooperation versus defection, distinct 947
      strategic signatures emerged for other linguistic contexts. The 948
      Chinese (cn) interactions demonstrated a notable preference 949
      for Tit-for-Tat (TFT) relative to other groups. This suggests 950
      that in the Chinese context, the model encodes a form of "con- 951
      ditional reciprocity" or relational fairness-mirroring cultural 952
      dynamics where cooperation is maintained through mutual 953
      exchange rather than blind altruism. In sharp contrast, the 954
      French (fr) agents displayed a significant divergence towards 955
      Win-Stay, Lose-Shift (WSLS). Unlike the rigid retaliation 956
      of TFT, WSLS operates on principles akin to reinforcement 957
      learning (repeating successful actions, switching only upon 958
      failure). This implies that the Francophone context primes the 959
      agents towards a more pragmatic, error-tolerant form of nego- 960
      tiation, prioritizing the restoration of stability over immediate 961
      punishment. These findings indicate that the "alignment" of 962
      an AI agent is not absolute but is deeply entangled with the 963
      cultural values embedded in the syntax and semantics of the 964
      prompt’s language. 965
      Figure A7: Strategy distribution across languages for multiple
      LLMs and the aggregated overview (baseline FAIRGAME dataset).
      Arabic consistently exhibits the highest ALLD rate; English and
      Chinese show strong WSLS preference; French tends toward cooperative strategies.
      Figure A8: The Language Effect. (Left) Average payoffs achieved
      by agents across linguistic settings. (Right) Strategy distribution
      revealing cultural heterogeneity: English prompts drive competitive defection (ALLD), Chinese prompts favor reciprocal strategies
      (TFT), while French prompts encourage adaptive, reinforcementlearning-style behaviors (WSLS), distinct from the high unconditional cooperation (ALLC) observed in Vietnamese.

+ TFT), which is due to its highest level of conditional co- 393
  operation (WSLS + TFT). Mistral Large shows the strongest 394
  unconditional cooperation bias, with ALLC being its most 395
  frequent strategy, though it retains diversity with ALLD and 396
  conditional behaviors. In contrast, GPT-4o exhibits a distinct 397
  “hawk” profile, with the highest defection rate. These dif- 398
  ferences persist across payoff scales and languages [Buscemi 399
  et al., 2025b; Fontana et al., 2025], suggesting that training 400
  procedures and alignment methods imprint distinct strategic 401
  priors: some models are inherently “dovish” while others are 402
  “hawkish.” 403
  Crucially, Figure 6 shows that these priors interact 404
  non-trivially with payoff scaling, revealing architecture- 405
  dependent incentive sensitivity. Across models, increasing 406
  λ systematically shifts behavior from unstable low-stake pat- 407
  terns toward stable strategies, though the extent of this shift 408
  varies by model. Claude and GPT-4o exhibit the highest pay- 409
  0.1 1 10
  Payoff Multiplier (λ)
  0
  10
  20
  30
  40
  50
  Percentage (%)
  31.8%
  18.2%
  21.8%
  28.1%
  Strategy Trends by Payoff Scale
  AllC
  AllD
  TFT
  WSLS
  Figure 5: Trends in inferred strategy distributions as a function of the
  payoff scaling parameter λ. Increasing payoff magnitude systematically shifts LLM behavior from unconditional defection (ALLD)
  toward conditional and cooperative strategies (WSLS, ALLC), indicating sensitivity to incentive scale.
  Strategy Overall Claude Mistral GPT-4o
  ALLC 29.1% 29.7% 33.7% 23.7%
  ALLD 25.9% 19.4% 25.2% 31.7%
  TFT 21.1% 25.1% 16.4% 22.8%
  WSLS 24.0% 25.8% 24.8% 21.9%
  Table 1: Overall (aggregate) and model-specific strategy distributions in the payoff-scaled experiments (three models:
  Claude 3.5 Haiku, Mistral Large and GPT-4o).
  410 off sensitivity: both models show steep reductions in ALLD
  411 prevalence as stakes move from attenuated to baseline lev412 els, effectively abandoning widespread defection when con413 sequences become non-trivial. GPT-4o is particularly respon414 sive, shifting from a strongly defect-heavy regime at low
  415 stakes to a more balanced profile at baseline. Mistral Large,
  416 by contrast, demonstrates strategic inertia: its ALLC rate
  417 varies by fewer than 5 percentage points across λ values,
  418 compared to GPT-4o’s ALLD shift of approximately 15 per419 centage points between attenuated and amplified conditions.
  420 This matches classical stake-effects where higher stakes am421 plify commitment to conventions, but highlights a critical nu422 ance for AI governance: some models (like GPT-4o) are es423 sentially rational agents that respond well to penalty tuning,
  424 while others (like Mistral) act as committed agents whose be425 havior is stubbornly invariant to incentive design [Fontana et
  426 al., 2025].
  Strategy Arabic Chinese Viet. English French
  ALLC 32% 31% 26% 26% 27%
  ALLD 28% 30% 24% 25% 18%
  TFT 19% 19% 23% 25% 26%
  WSLS 21% 20% 27% 24% 29%
  Table 2: Strategy distribution (%) across languages. Arabic and Chinese favour unconditional strategies (ALLC+ALLD > 50%), while
  French and Vietnamese favour adaptive reciprocity (TFT+WSLS).
  427 A notable finding is the significant influence of linguistic
  0
  20
  40
  Percentage (%)
  Claude 3.5 Mistral
  0.1 1 10
  Payoff Multiplier (λ)
  0
  20
  40
  Percentage (%)
  GPT-4o
  Strategy Trends Across LLMs and Payoff Scales
  AllC
  AllD
  TFT
  WSLS
  Figure 6: Interaction between payoff scaling and LLM architecture.
  Each subplot illustrates how inferred strategies evolve with increasing payoff magnitude for a given model, revealing heterogeneous
  incentive sensitivity across LLMs.
  context on strategic behavior, an effect we term linguistic- 428
  cultural priming. Table 2 reveals that languages cluster into 429
  distinct strategic archetypes. Arabic and Chinese exhibit a 430
  shared bias toward unconditional strategies, with combined 431
  ALLC+ALLD exceeding 60%. In contrast, French exhibits 432
  the most conditional profile, with agents preferring respon- 433
  sive play. English occupies an intermediate position with a 434
  uniform distribution, likely reflecting its dominance in train- 435
  ing corpora [Buscemi et al., 2025c]. 436
  Moreover, these linguistic priming effects interact dynam- 437
  ically with incentive magnitude (Figure 7). Arabic and 438
  Vietnamese exhibit significant stake-sensitivity: defection- 439
  oriented behavior at low stakes gives way to cooperation as 440
  consequences amplify, suggesting that culturally-primed de- 441
  fection biases can be overridden by sufficiently strong incen- 442
  tives. French, by contrast, maintains its cooperative norms 443
  regardless of stakes, a form of cultural inertia that resists in- 444
  centive pressure. Notably, at high stakes, English and French 445
  converge to nearly identical strategic profiles, suggesting that 446
  sufficiently strong incentives can normalize cross-linguistic 447
  variation. This has important implications for AI deploy- 448
  ment: while language choice may introduce behavioral bi- 449
  ases at low stakes, high-stakes environments may naturally 450
  mitigate some of these effects. 451
  0
  20
  40
  Percentage (%)
  English Chinese
  0
  20
  40
  Percentage (%)
  Arabic French
  0.1 1 10
  Payoff Multiplier (λ)
  0
  20
  40
  Percentage (%)
  Vietnamese
  Strategy Trends Across Languages and Payoff Scales
  AllC
  AllD
  TFT
  WSLS
  Figure 7: Interaction between payoff scaling and language. Each
  subplot shows strategy evolution as λ increases from 0.1 to 10. Arabic and Vietnamese show strong stake-sensitivity, while French exhibits stable conditional behaviors across all conditions.
  452 3.3 Statistical Validation
  453 To move beyond descriptive statistics, we conducted for454 mal hypothesis testing using chi-square tests and factorial
  455 ANOVA. The results confirm that stake level significantly af456 fects strategy distributions, and that different LLM architec457 tures exhibit distinct incentive sensitivities. Post-hoc com458 parisons reveal the largest behavioral differences between at459 tenuated and amplified stake conditions, with moderate ef460 fect sizes consistent with the inherent stochasticity of LLM
  461 decision-making [Fontana et al., 2025]. These statistical val462 idations support our core finding: LLM strategic behavior is
  463 systematically, i.e. not merely randomly, influenced by in464 centive design.
  465 Our statistical tests treat trajectories as independent obser466 vations; however, the experimental design introduces nested
  467 dependencies: 10 repetitions per condition, 10 rounds per
  468 game, and 2 agents per game. For the chi-square test, the de469 pendent variable is strategy category (4 levels); for ANOVA,
  470 we use a numeric encoding (ALLC=1, TFT=2, WSLS=3,
  471 ALLD=4) aggregated at the trajectory level. Mixed-effects
  472 multinomial logistic regression with random intercepts for
  473 repetition and game instance would better account for this
  474 nested structure and categorical outcomes; we acknowledge
  475 this as a methodological limitation. Our fixed-effects ap476 proach provides conservative estimates given consistent ef477 fect directions across conditions, and bootstrap-based robust478 ness checks (Supplementary Material, Section 1.6) confirm
  479 the stability of our conclusions.
  480 Deep learning models (LSTM, Neural Network) outper481 form probabilistic models (HMM, State-Factorized) on conTable 3: Statistical validation summary: (a) hypothesis tests for
  stake effects, (b) classifier comparison for strategy recognition
  (n=80,640 test samples, 4-strategy, 5% noise).
  (a) Stake Effect Tests
  Test Statistic p Effect Sig.
  Chi-Square χ
  2
  (6) = 32.59 < .001 V = 0.065 ***
  1-Way ANOVA F(2, 3825) = 3.80 < .001 η
  2 = 0.005 ***
  2-Way ANOVA F = 31.69 < .001 R
  2 = 0.024 ***
  (b) Classifier Performance
  Model Acc. Prec. Rec. F1
  LSTM 0.984 0.984 0.984 0.984
  Random Forest 0.980 0.980 0.980 0.980
  State-Factorized 0.956 0.958 0.956 0.956
  Neural Network 0.937 0.937 0.937 0.937
  HMM 0.777 0.826 0.777 0.780
  Logistic Reg. 0.756 0.767 0.756 0.751
  ditional strategies (TFT: LSTM 0.98 vs HMM 0.74; WSLS: 482
  LSTM 0.98 vs HMM 0.73), justifying our methodological 483
  choice. The State-Factorized model [Fontana et al., 2025] 484
  achieves 0.956 accuracy, providing a strong SFEM-style 485
  baseline. While SFEM excels at estimating mixture propor- 486
  tions over long horizons (100+ rounds), our LSTM approach 487
  trades mixture flexibility for interpretable point estimates on 488
  shorter sequences. 489
  The LSTM achieves near-perfect performance on uncondi- 490
  tional strategies (ALLC/ALLD: F1 = 0.99) but exhibits mod- 491
  est confusion between TFT and WSLS under noise, where 492
  execution errors can blur characteristic signatures. The Hid- 493
  den Markov Model (HMM) baseline shows much higher con- 494
  fusion on conditional strategies (F1 ≈ 0.74), justifying our 495
  LSTM choice. Confidence scores are uncalibrated; thresh- 496
  old sensitivity analysis (Supplementary Material, Section 1.5) 497
  shows robustness across τ ∈ [0.7, 0.95]. 498
  4 Discussion and Conclusion 499
  This work successfully establishes a unified framework for 500
  auditing LLMs as strategic agents, integrating game-theoretic 501
  benchmarking with supervised learning based intent recogni- 502
  tion. Our findings demonstrate that LLM behavior is not a 503
  static property but a dynamic and interpretable response to 504
  key contextual factors: incentive magnitude, model architec- 505
  ture, and linguistic framing. We reveal that LLMs exhibit 506
  systematic incentive sensitivity, becoming more cooperative 507
  as stakes amplify, while also displaying distinct cultural char- 508
  acteristics where the language of interaction can prime them 509
  towards either committed or adaptively reciprocal strategies. 510
  These insights carry immediate and significant implica- 511
  tions for AI governance and the design of multi-agent sys- 512
  tems. Our results highlight that traditional safety audits, often 513
  conducted in English under fixed conditions, are insufficient 514
  to capture strategy shifts driven by incentives and linguistic 515
  context. A model deemed safe and cooperative in one linguis- 516
  tic or incentive context may exhibit aggressive or uncooper- 517
  ative behavior in another. Effective governance therefore re- 518
  quires comprehensive stress-testing of LLM agents across di- 519
  verse incentive regimes and linguistic environments to proac- 520
  521 tively identify and mitigate these latent behavioral patterns.
  522 Several limitations warrant acknowledgement. First, our
  523 intent classifier covers four canonical strategies; trajectories
  524 exhibiting mixed policies, Zero-Determinant strategies [Press
  525 and Dyson, 2012; Hilbe et al., 2013], or extortionate play
  526 may be misattributed to the nearest canonical archetype, po527 tentially inflating WSLS or TFT rates in ambiguous cases.
  528 Second, the 10-round horizon limits detection of sophisti529 cated conditional strategies that require longer interaction
  530 histories to manifest and stabilize. Third, we use provider531 recommended temperature settings and uncalibrated confi532 dence thresholds, which may introduce variability confounds;
  533 however, our ∼90% high-confidence retention rate suggests
  534 robust classifier coverage. Effect sizes are modest (Cramér’s
  535 V ≈ 0.065) but practically significant given compounding in
  536 deployed multi-agent systems. Future work can extend the
  537 strategy space, apply calibration, conduct temperature abla538 tions, and benchmark against human data.
  539 The study also points to several promising avenues for fu540 ture research. Extending experiments to longer interaction
  541 horizons and incorporating reasoning traces would enable
  542 the capture of more complex and emergent strategic dynam543 ics. Benchmarking LLM behavior against human behavioral
  544 data would provide essential context for assessing whether
  545 these strategies emulate, deviate from, or transcend human
  546 decision-making patterns. Further investigation of opponent
  547 shaping and workflow scaffolding could shed light on how
  548 LLMs adapt their strategies in response to dynamic interac549 tion partners. Finally, expanding the analysis to asymmet550 ric and multi-player games with inter-agent communication
  551 would enable a richer understanding of LLM behavior in
  552 complex social dilemmas.
  553 In conclusion, this work shows that language and incen554 tives are not peripheral implementation details but fundamen555 tal control variables shaping LLM strategic behavior. LLMs
  556 do not possess a single, intrinsic policy; instead, their strate557 gies emerge from the interaction between model architecture,
  558 incentive structure, and linguistic framing. As LLMs are in559 creasingly deployed in high-stakes economic and social roles,
  560 recognizing and accounting for these dynamics becomes es561 sential. Understanding how strategies shift across contexts
  562 will be as critical as model architecture or training data in en563 suring reliable, effective, and ethically aligned multi-agent AI
  564 systems.
  565 References
  566 [Akata et al., 2025] Elif Akata, Lion Schulz, Julian Coda567 Forno, Seong Joon Oh, Matthias Bethge, and Eric Schulz.
  568 Playing repeated games with large language models. Na569 ture Human Behaviour, pages 1–11, 2025.
  570 [Anthropic, 2024] Anthropic. Introducing the next genera571 tion of claude.
  572 urlhttps://www.anthropic.com/news/claude-3-family,
  573 2024. Accessed: 2025-01-02.
  574 [Axelrod, 1980] Robert Axelrod. Effective choice in the
  575 prisoner’s dilemma. The Journal of Conflict Resolution,
  576 24(3):379–403, 1980.
  [Bai et al., 2022] Yuntao Bai, Saurav Kadavath, Sandipan 577
  Kundu, Amanda Askell, Jackson Kernion, Andy Jones, 578
  Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron 579
  McKinnon, et al. Constitutional ai: Harmlessness from 580
  ai feedback. arXiv preprint arXiv:2212.08073, 2022. 581
  [Breiman, 2001] Leo Breiman. Random forests. Mach. 582
  Learn., 45(1):5–32, October 2001. 583
  [Buscemi et al., 2025a] Alessio Buscemi, Daniele Prover- 584
  bio, Paolo Bova, Nataliya Balabanova, Adeela Bashir, 585
  Theodor Cimpeanu, et al. Do LLMs trust AI regula- 586
  tion? Emerging behaviour of game-theoretic LLM agents. 587
  arXiv:2504.08640, 2025. 588
  [Buscemi et al., 2025b] Alessio Buscemi, Daniele Prover- 589
  bio, Alessandro Di Stefano, The Anh Han, German Castig- 590
  nani, and Pietro Liò. Fairgame: a framework for ai agents 591
  bias recognition using game theory. Frontiers in Artificial 592
  Intelligence and Applications (ECAI 2025), pages 4097– 593
  4104, 2025. 594
  [Buscemi et al., 2025c] Alessio Buscemi, Daniele Prover- 595
  bio, Alessandro Di Stefano, The Anh Han, German Cas- 596
  tignani, and Pietro Liò. Strategic communication and lan- 597
  guage bias in multi-agent llm coordination. In Interna- 598
  tional Conference on Multi-disciplinary Trends in Artifi- 599
  cial Intelligence, pages 289–301. Springer, 2025. 600
  [Cox, 1958] David R Cox. The regression analysis of binary 601
  sequences. Journal of the Royal Statistical Society: Series 602
  B (Methodological), 20(2):215–232, 1958. 603
  [Di Stefano et al., 2023] Alessandro Di Stefano, Chrisina 604
  Jayne, Claudio Angione, and The Anh Han. Recogni- 605
  tion of behavioural intention in repeated games using ma- 606
  chine learning. In Artificial Life Conference Proceedings 607
  35, page 103. MIT Press, 2023. 608
  [Fan et al., 2024] Caoyun Fan, Jindou Chen, Yaohui Jin, and 609
  Hao He. Can large language models serve as rational play- 610
  ers in game theory? a systematic analysis. In Proc. AAAI 611
  Conference on Artificial Intelligence, volume 38, pages 612
  17960–17967, 2024. 613
  [Fontana et al., 2025] Nicoló Fontana, Francesco Pierri, and 614
  Luca Maria Aiello. Nicer than humans: How do large 615
  language models behave in the prisoner’s dilemma? In 616
  Proceedings of the International AAAI Conference on Web 617
  and Social Media (ICWSM), 2025. 618
  [Fujimoto and Kaneko, 2019] Yuma Fujimoto and Kunihiko 619
  Kaneko. Functional dynamic by intention recognition in 620
  iterated games. New Journal of Physics, 21(2):023025, 621

2019. 622
      [Hammond et al., 2025] Lewis Hammond, Alan Chan, Jesse 623
      Clifton, Jason Hoelscher-Obermaier, Akbir Khan, Euan 624
      McLean, Chandler Smith, Wolfram Barfuss, Jakob Foer- 625
      ster, Tomáš Gavenciak, et al. Multi-Agent Risks from Ad- ˇ 626
      vanced AI. arXiv preprint arXiv:2502.14143, 2025. 627
      [Han et al., 2011] The Anh Han, Luís Moniz Pereira, and 628
      Francisco C Santos. The role of intention recognition in 629
      the evolution of cooperative behavior. In Proceedings of 630
      the Twenty-Second international joint conference on Arti- 631
      ficial Intelligence (IJCAI), pages 1684–1689, 2011. 632
      633 [Han et al., 2012] The Anh Han, Luís Moniz Pereira, and
      634 Francisco C. Santos. Corpus-based intention recognition
      635 in cooperation dilemmas. Artificial Life, 18(4):365–383,
      636 10 2012.
      637 [Han et al., 2021] The Anh Han, Cedric Perret, and Simon T.
      638 Powers. When to (or not to) trust intelligent machines:
      639 Insights from an evolutionary game theory analysis of trust
      640 in repeated games. Cognitive Systems Research, 68:111–
      641 124, August 2021.
      642 [Hilbe et al., 2013] Christian Hilbe, Martin A Nowak, and
      643 Karl Sigmund. Evolution of extortion in iterated prisoner’s
      644 dilemma games. Proceedings of the National Academy of
      645 Sciences, 110(17):6913–6918, 2013.
      646 [Hochreiter and Schmidhuber, 1997] Sepp Hochreiter and
      647 Jürgen Schmidhuber. Long short-term memory. Neural
      648 Computation, 9(8):1735–1780, 11 1997.
      649 [Hua et al., 2024] Wenyue Hua, Ollie Liu, Lingyao Li, Al650 fonso Amayuelas, Julie Chen, Lianhui Jiang, et al. Game651 theoretic LLM: Agent workflow for negotiation games,
      652 2024.
      653 [Hurst et al., 2024] Aaron Hurst, Adam Lerer, Adam P.
      654 Goucher, et al. GPT-4o system card, 2024.
      655 [Jiang et al., 2023] Albert Q. Jiang, Alexandre Sablayrolles,
      656 Arthur Mensch, Chris Bamford, Devendra Singh Chaplot,
      657 Diego de las Casas, Florian Bressand, Gianna Lengyel,
      658 Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud,
      659 Marie-Anne Lachaux, Pierre Stock, Teven Le Scao,
      660 Thibaut Lavril, Thomas Wang, Timothée Lacroix, and
      661 William El Sayed. Mistral 7b, 2023.
      662 [Jordan and Bishop, 1996] Michael I. Jordan and Christo663 pher M. Bishop. Neural networks. ACM Comput. Surv.,
      664 28(1):73–75, March 1996.
      665 [Krockow et al., 2016] Eva M Krockow, Andrew M Colman,
      666 and Briony D Pulford. Cooperation in repeated inter667 actions: A systematic review of centipede game experi668 ments, 1992–2016. European Review of Social Psychol669 ogy, 27(1):231–282, 2016.
      670 [List, 2006] John A List. Friend or foe? a natural experiment
      671 of the prisoner’s dilemma. The Review of Economics and
      672 Statistics, 88(3):463–471, 2006.
      673 [Lorè and Heydari, 2024] Nicola Lorè and Behnam Heydari.
      674 Strategic behavior of large language models and the role
      675 of game structure versus contextual framing. Scientific Re676 ports, 2024.
      677 [Lu et al., 2024] Yikang Lu, Alberto Aleta, Chunpeng Du,
      678 Lei Shi, and Yamir Moreno. Llms and generative agent679 based models for complex systems research. Phys. Life
      680 Rev., 2024.
      681 [Mao et al., 2025] Shaoguang Mao, Yuzhe Cai, Yan Xia,
      682 Wenshan Wu, Xun Wang, Fengyi Wang, Qiang Guan, Tao
      683 Ge, and Furu Wei. Alympics: Llm agents meet game the684 ory. In Proceedings of the 31st International Conference
      685 on Computational Linguistics, pages 2845–2866, 2025.
      [Montero-Porras et al., 2022] Eladio Montero-Porras, Jelena 686
      Grujic, Elias Fernández Domingos, and Tom Lenaerts. In- ´ 687
      ferring strategies from observations in long iterated pris- 688
      oner’s dilemma experiments. Scientific Reports, 12, 05 689
2020. 690
      [Ouyang et al., 2022] Long Ouyang, Jeffrey Wu, Xu Jiang, 691
      Diogo Almeida, Carroll Wainwright, Pamela Mishkin, 692
      Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex 693
      Ray, et al. Training language models to follow instruc- 694
      tions with human feedback. Advances in Neural Informa- 695
      tion Processing Systems, 35:27730–27744, 2022. 696
      [Pal et al., 2026] Saptarshi Pal, Abhishek Mallela, Chris- 697
      tian Hilbe, Lenz Pracher, Chiyu Wei, Feng Fu, Santiago 698
      Schnell, and Martin A Nowak. Strategies of cooperation 699
      and defection in five large language models. arXiv preprint 700
      https://arxiv.org/abs/2601.09849, 2026. 701
      [Pires et al., 2025] Alexandre S Pires, Laurens Samson, Sen- 702
      nay Ghebreab, and Fernando P Santos. How large lan- 703
      guage models judge and influence human cooperation. 704
      arXiv preprint arXiv:2507.00088, 2025. 705
      [Press and Dyson, 2012] William H Press and Freeman J 706
      Dyson. Iterated prisoner’s dilemma contains strategies 707
      that dominate any evolutionary opponent. Proceedings of 708
      the National Academy of Sciences, 109(26):10409–10413, 709
2021. 710
      [Sigmund, 2010] K. Sigmund. The calculus of selfishness. 711
      Princeton Univ. Press, 2010. 712
      [Sun and others, 2025] Yutong Sun et al. Game theory meets 713
      large language models: A survey. In Proceedings of the 714
      Thirty-Fourth International Joint Conference on Artificial 715
      Intelligence (IJCAI-25) Survey Track, 2025. 716
      [Tessler et al., 2024] Michael Henry Tessler, Michiel A 717
      Bakker, Daniel Jarrett, Hannah Sheahan, Martin J Chad- 718
      wick, et al. Ai can help humans find common ground 719
      in democratic deliberation. Science, 386(6719):eadq2852, 720
2022. 721
      [Willis et al., 2025] Richard Willis, Yali Du, and Joel Z 722
      Leibo. Will systems of llm agents lead to cooperation: 723
      An investigation into a social dilemma. In Proceedings of 724
      the 24th International Conference on Autonomous Agents 725
      and Multiagent Systems, pages 2786–2788, 2025. 726
      727 A Supplement to Methodology
      728 A.1 LLM Configuration
      729 Table A1 summarizes the configuration of LLM backends
      730 used in our experiments. Following the FAIRGAME proto731 col [Buscemi et al., 2025b], we adopt each provider’s recom732 mended default settings to reflect realistic deployment condi733 tions.
      Model Provider Temperature Top_p
      GPT-4o OpenAI 1.0 1.0
      Claude 3.5 Haiku Anthropic 1.0 1.0
      Mistral Large Mistral AI 0.3 1.0
      Table A1: LLM backend configurations. Temperature and sampling
      parameters follow each provider’s recommended defaults. While
      this introduces potential variability confounds in cross-model comparisons, it reflects realistic deployment conditions where practitioners use models “out of the box.”
      734 A.2 Payoff Scaling Examples
      735 For illustration, the scaled payoff matrices under the three
      736 experimental conditions are shown below. When λ = 0.1
      737 (attenuated stakes), the row player’s payoff matrix becomes:
      Option A Option B
      Option A (0.6, 0.6) (0, 1.0)
      Option B (1.0, 0) (0.2, 0.2)
      738 When λ = 10.0 (amplified stakes), it becomes:
      Option A Option B
      Option A (60, 60) (0, 100)
      Option B (100, 0) (20, 20)
      739 The ordering T < R < P < S is preserved in all cases,
      740 ensuring the strategic structure of the Prisoner’s Dilemma
      741 remains unchanged while only the magnitude of incentives
      742 varies.
      743 A.3 Rule-Based Strategy Assignment
      744 To complement the LSTM-based strategy predictions and ad745 dress cases where behavioral patterns exhibit characteristics
      746 of multiple canonical strategies, we apply deterministic rule747 based algorithms to identify all potential strategy labels con748 sistent with observed action sequences. These rules encode
      749 the defining characteristics of each strategy as logical condi750 tions on the agent’s action trajectory a = (a1, a2, . . . , aT )
      751 and the opponent’s history o = (o1, o2, . . . , oT ).
      752 Always Cooperate (ALLC): The agent cooperates in all
      753 rounds regardless of opponent behaviour.
      ALLC ≡ ∀t ∈ {1, . . . , N} : at = C
      754 Always Defect (ALLD): The agent defects in all rounds
      755 regardless of opponent behaviour.
      ALLD ≡ ∀t ∈ {1, . . . , N} : at = D
      Tit-for-Tat (TFT): The agent cooperates in round 1, then 756
      copies the opponent’s previous action. To accommodate ex- 757
      ecution errors, we tolerate up to ϵnoise deviations from pure 758
      TFT logic. 759
      TFT ≡ (a1 = C) ∧
      X
      N
      t=2
      I[at ̸= ot−1] ≤ ϵnoise · (N − 1)!
      where I[·] is the indicator function and ϵnoise = 0.1 in our 760
      implementation. 761
      Win-Stay-Lose-Shift (WSLS): The agent repeats its pre- 762
      vious action if the outcome was a Reward (R, mutual co- 763
      operation) or Temptation (Temp, successful defection), and 764
      switches otherwise. The initial action can be either C or D. 765
      Similarly, we tolerate up to ϵnoise deviations. 766
      Let aˆt =
      
      at−1 if (at−1, ot−1) ∈ {(C, C),(D, C)}
      ¬at−1 if (at−1, ot−1) ∈ {(C, D),(D, D)}
      WSLS ≡
      X
      N
      t=2
      I[at ̸= ˆat] ≤ ϵnoise · (N − 1)
      These rules are applied sequentially to each trajectory. A tra- 767
      jectory may receive multiple labels if it satisfies conditions for 768
      overlapping strategies (e.g., a short sequence of all-cooperate 769
      satisfies both ALLC and TFT). To avoid double-counting in 770
      aggregate statistics, we apply a priority ordering: pure un- 771
      conditional strategies (ALLD, ALLC) take precedence over 772
      conditional ones (TFT, WSLS), reflecting their simpler gen- 773
      erative structure. The hybrid pipeline combines these rule- 774
      based assignments with LSTM predictions: high-confidence 775
      LSTM outputs (τ ≥ 0.9) are retained, while ambiguous cases 776
      (τ < 0.9) are supplemented with rule-based labels when ap- 777
      plicable. In our corpus, 4.2% of trajectories received multiple 778
      candidate labels before priority resolution. This approach en- 779
      sures both coverage (via rules for unambiguous patterns) and 780
      robustness (via LSTM for noisy, complex cases). 781
      A.4 High-Confidence Filtering Rationale 782
      We employed a selective filtering approach to ensure the re- 783
      liability of our LLM behavioural strategy analysis. Specifi- 784
      cally, we focused our analysis on game instances where the 785
      predicted strategy labels for both agents exhibited prediction 786
      probabilities exceeding 0.9 (90% confidence threshold). The 787
      decision to use high-confidence predictions is grounded in 788
      several key considerations: 789
      • Pattern Alignment with Theoretical Strategies: Sam- 790
      ples with prediction probabilities above 0.9 indicate that 791
      the observed behavioural sequences of LLMs closely 792
      align with the canonical patterns defined by the four 793
      classical strategies (ALLD, ALLC, WSLS, and TFT). 794
      • Signal-to-Noise Separation: While the probabilities 795
      are not absolute (not reaching 1.0), this is expected and 796
      attributable to inherent noise in LLM decision-making 797
      processes. 798
      • Statistical Reliability: By focusing on high-confidence 799
      predictions, we minimize the risk of misclassification 800
      and ensure that our strategy distribution analysis reflects 801
      genuine behavioural patterns. 802
      803 A.5 Threshold Sensitivity Analysis
      804 To validate our choice of confidence threshold τ = 0.9,
      805 we conducted a systematic sensitivity analysis across τ ∈
      806 [0.3, 0.95] for 3-, 4-, and 5-strategy classification models.
      807 Figure A1 illustrates how retention rate, average confidence,
      808 number of predictions retained, and strategy diversity vary as
      809 a function of threshold value.
      Figure A1: Comprehensive threshold sensitivity analysis for payoffscaled experiments. Top row: retention rate and average confidence
      vs. threshold. Bottom row: number of predictions retained and strategy diversity. The 4-strategy model at τ = 0.9 provides optimal balance between coverage (58.5% retention) and reliability (avg. confidence 0.99).
      810 Table A2 summarises key metrics at τ = 0.9:
      Metric 3-Strat 4-Strat 5-Strat
      Retention Rate 78.3% 58.5% 53.2%
      Avg Confidence 0.989 0.985 0.978
      Diversity 3 4 4
      Table A2: Threshold sensitivity at τ = 0.9 across strategy models.
      811 Key findings: (1) Retention rate decreases as strategy space
      812 expands, reflecting greater behavioral complexity; (2) Aver813 age confidence remains > 0.97 at τ = 0.9 across all models;
      814 (3) Lowering to τ = 0.7 would increase retention to 75–87%
      815 but reduce average confidence to 0.94–0.97. Our choice of
      816 τ = 0.9 prioritizes classification reliability while maintain817 ing sufficient coverage for statistical analysis.
      818 A.6 Model Robustness to Noise
      819 We first evaluated the robustness of different classifier archi820 tectures against execution noise, which simulates the stochas821 ticity and potential “hallucinations” of LLMs. As shown in
      822 Figure A2, while Logistic Regression (LR) and Random For823 est (RF) models achieved near-perfect accuracy (greater than
      824 0.9) on clean data, their performance degraded when intro825 duced to 5% execution noise. In contrast, the Long Short826 Term Memory (LSTM) network maintained the highest ac827 curacy (∼ 94%). This superiority stems from the LSTM’s
      Figure A2: Model Robustness to Noise. Comparison of Accuracy
      and F1-Score between Logistic Regression, Random Forest, and
      LSTM on No-Noise and Noise 0.05 datasets. The LSTM demonstrates superior resilience to execution noise.
      recurrent architecture, which allows it to learn the sequential 828
      “context” of a strategy, effectively “forgiving” random devia- 829
      tions to identify the core behavioral pattern. 830
      B Supplement to Results 831
      B.1 Payoff-Scaled Experiments: Additional 832
      Analyses 833
      This section provides supplementary analyses for the payoff- 834
      scaled Prisoner’s Dilemma experiments (see main paper). 835
      Per-Multiplier Behavioral Metrics To visualize the be- 836
      havioral profiles of different LLM architectures across pay- 837
      off scaling conditions, we present radar charts comparing 838
      normalized metrics for each multiplier setting. Figure A3 839
      displays four key behavioural dimensions-internal variabil- 840
      ity (IV), cross-language-inconsistency (CI), variability over 841
      round (VR), and sensitivity-to-payoff (SP)-normalized within 842
      each multiplier condition to enable direct cross-model com- 843
      parison. 844
      Key observations include: (1) At attenuated stakes (λ = 845
      0.1), the three models display maximally divergent behav- 846
      ioral signatures, with Claude 3.5 Haiku exhibiting elevated 847
      Variation Rate while GPT-4o shows stronger Cooperation In- 848
      dex; (2) At baseline stakes (λ = 1), models begin to con- 849
      verge toward more balanced profiles; (3) At amplified stakes 850
      (λ = 10), all models shift toward higher CI and SP values, 851
      suggesting that increased consequences promote both coop- 852
      erative behaviour and strategic consistency. These radar visu- 853
      alizations complement the line plots in the main paper by pro- 854
      viding a holistic view of multi-dimensional behavioral shifts. 855
      Multidimensional Behavioral Comparison The visual- 856
      ization in Figure A4 provides a synoptic view of how the 857
      three cardinal dimensions of our study—payoff magnitude, 858
      linguistic context, and model architecture—interact to shape 859
      agent behavior. By synthesizing these factors, we observe 860
      that strategic behavior is not driven by a single determinant 861
      but emerges from their complex interplay. Notably, the vari- 862
      ance attributable to linguistic context (visualized across the 863
      language axes) often rivals or even exceeds the variance be- 864
      tween distinct model architectures, challenging the notion 865
      of fixed, immutable “model personalities.” Furthermore, 866
      the impact of payoff scaling is shown to be non-uniform; 867
      while amplified stakes generally compress behavioral diver- 868
      sity towards cooperation, the specific trajectory of this shift 869
      is heavily modulated by the language in which the game is 870
      Figure A3: Per-Multiplier Behavioural Metrics. We report four standardized metrics defined in the FAIRGAME framework [Buscemi et al.,
      2025b]: (1) Internal Variability (IV), which quantifies the stochasticity of an agent’s behavior by measuring the variance of outcomes across
      identical experimental repetitions; (2) Cross-Language Inconsistency (CI), which measures the standard deviation of agent performance
      across the five tested languages to indicate sensitivity to linguistic framing; (3) Variability over Round (VR), which captures the volatility
      of decision-making and strategy changes throughout the 10-round game horizon; and (4) Sensitivity-to-Payoff (SP), which reflects the
      magnitude of behavioral adaptation in response to varying incentive stakes. Radar charts comparing Mistral Large (green), Claude 3.5 Haiku
      (orange), and GPT-4o (blue) across three payoff scales (λ ∈ {0.1, 1, 10}). Compared to the baseline payoff (λ = 1), similar scores are
      observed for the higher stake payoff (λ = 10). At low stakes (λ = 0.1), models exhibit divergent scores. Overall, internal variability (IV) is
      most affected by varying the payoff stake.
      871 framed. This suggests that alignment interventions must ac872 count for this multidimensional sensitivity, as a model aligned
      873 for safety in English may exhibit divergent, risk-seeking be874 haviors when prompted in other languages or under different
      875 incentive structures.
      876 Unconditional vs Conditional Strategy Aggregation To
      877 provide a higher-level view of strategic tendencies across lin878 guistic contexts, we aggregate the four canonical strategies
      879 into two categories: unconditional (ALLC + ALLD) and con880 ditional (TFT + WSLS). This aggregation reveals whether
      881 agents commit to fixed policies regardless of opponent be882 haviour, or adapt their strategies based on interaction history.
      883 As shown in Figure A5, Arabic and Chinese prompts
      884 elicit predominantly unconditional behaviour (exceeding
      885 60% combined ALLC+ALLD), while French demonstrates
      886 the most conditional profile with over 55% of agents adopt887 ing TFT or WSLS strategies. This pattern corroborates the
      888 fine-grained analysis in the main paper, suggesting that lin889 guistic context systematically modulates the degree to which
      890 LLM agents engage in adaptive versus committed strategic
      891 behaviour.
      892 B.2 Baseline FAIRGAME Analysis: Detailed
      893 Results
      894 This appendix presents the complete analysis of LLM strate895 gic behaviour from the baseline FAIRGAME dataset, com896 plementing the payoff-scaled experiments in the main text.
      897 The dataset covers four LLM models-Claude 3.5 Sonnet,
      898 Llama 3.1 405B Instruct, Mistral Large, and GPT-4o-across
      899 five languages (Arabic, Chinese, English, French, and Viet900 namese).
      Hybrid Classification Approach While our LSTM model 901
      demonstrates strong performance in strategy classification, it 902
      was originally designed as a single-label classifier. To address 903
      this limitation and ensure comprehensive coverage, we adopt 904
      a hybrid labeling approach that combines model predictions 905
      with rule-based strategy assignment (see Appendix A.3). 906
      Strategy Distribution Across Models The strategic pref- 907
      erence analysis from the baseline FAIRGAME dataset re- 908
      veals significant heterogeneity in decision-making paradigms 909
      across LLM architectures. Claude 3.5 Sonnet exhibits 910
      a cooperative-dominant behavioural pattern, with ALLC 911
      (31.7%) and WSLS (29.6%) emerging as its two most fre- 912
      quent strategies. Llama 3.1 405B Instruct is characterized 913
      by a pronounced preference for WSLS (46.5%), the highest 914
      proportion of any single strategy across all evaluated mod- 915
      els. Mistral Large demonstrates the most balanced strate- 916
      gic distribution, with TFT (29.9%), ALLC (26.1%), WSLS 917
      (24.3%), and ALLD (19.7%) occurring at comparable rates. 918
      Finally, GPT-4o shows an adaptive-cooperative profile in this 919
      dataset, primarily using WSLS (34.1%) and ALLC (26.4%), 920
      with ALLD at 10.2%.1
      921
      Language Effects on Strategies A striking finding is the 922
      profound impact of the language of interaction on strategic 923
      choice. Arabic consistently shows the highest proportion 924
      of ALLD, followed by Vietnamese, indicating a strong ten- 925
      dency toward non-cooperative behaviour. French and Chi- 926
      1Note: GPT-4o exhibits higher ALLD rates (31.7%) in the
      payoff-scaled experiments (see main paper), which use different experimental conditions and payoff magnitudes. This difference reflects the context-dependent nature of LLM strategic behaviour.
      Figure A4: Multidimensional comparison of LLM behavioral strategies across payoff scales, languages, and model architectures. The figure
      synthesizes incentive sensitivity, linguistic priming, and architectural bias, illustrating that language effects can rival or exceed model-level
      differences.
      Figure A5: Unconditional versus conditional strategy aggregation
      across languages (payoff-scaled experiments). Arabic and Chinese
      exhibit the highest unconditional rates (>60%), while French shows
      the most conditional profile (>55% TFT+WSLS). This aggregated
      view complements the language strategy distribution table in the
      main paper.
      927 nese demonstrate relatively stronger cooperative tendencies.
      928 Despite variations in absolute percentages, the relative order929 ing of languages remains remarkably stable across all models.
      930 Strategy Recognition via Supervised Machine Learning
      931 The Language Effect (Baseline Dataset): Note that the
      932 following analysis is from the baseline FAIRGAME dataset
      933 (Claude 3.5 Sonnet, Llama, GPT-4o, Mistral), which differs
      934 from the payoff-scaled experiments in the main paper. Dif935 ferences in language characterizations reflect dataset-specific
      936 patterns.
      937 As illustrated in Figure A8, English interactions were
      938 characterized by a hyper-competitive baseline, exhibiting the
      939 highest density of Always Defect (ALLD) strategies and the
      940 lowest rates of adaptive cooperation. This behaviour likely
      941 reflects the dominance of game-theoretic and individualis942 tic maximizing narratives in the Anglo-centric training cor943 pus. Conversely, Vietnamese prompts elicited the highest
      944 frequency of unconditional cooperation (ALLC), consistent
      945 with the hypothesis that the model retrieves collectivist or
      Figure A6: Strategic behavioural distribution across four LLMs in iterated Prisoner’s Dilemma gameplay. The analysis is based on highconfidence predictions (probability > 0.9) from our trained classification model.
      community-oriented norms associated with the language. 946
      Beyond the binary of cooperation versus defection, distinct 947
      strategic signatures emerged for other linguistic contexts. The 948
      Chinese (cn) interactions demonstrated a notable preference 949
      for Tit-for-Tat (TFT) relative to other groups. This suggests 950
      that in the Chinese context, the model encodes a form of "con- 951
      ditional reciprocity" or relational fairness-mirroring cultural 952
      dynamics where cooperation is maintained through mutual 953
      exchange rather than blind altruism. In sharp contrast, the 954
      French (fr) agents displayed a significant divergence towards 955
      Win-Stay, Lose-Shift (WSLS). Unlike the rigid retaliation 956
      of TFT, WSLS operates on principles akin to reinforcement 957
      learning (repeating successful actions, switching only upon 958
      failure). This implies that the Francophone context primes the 959
      agents towards a more pragmatic, error-tolerant form of nego- 960
      tiation, prioritizing the restoration of stability over immediate 961
      punishment. These findings indicate that the "alignment" of 962
      an AI agent is not absolute but is deeply entangled with the 963
      cultural values embedded in the syntax and semantics of the 964
      prompt’s language. 965
      Figure A7: Strategy distribution across languages for multiple
      LLMs and the aggregated overview (baseline FAIRGAME dataset).
      Arabic consistently exhibits the highest ALLD rate; English and
      Chinese show strong WSLS preference; French tends toward cooperative strategies.
      Figure A8: The Language Effect. (Left) Average payoffs achieved
      by agents across linguistic settings. (Right) Strategy distribution
      revealing cultural heterogeneity: English prompts drive competitive defection (ALLD), Chinese prompts favor reciprocal strategies
      (TFT), while French prompts encourage adaptive, reinforcementlearning-style behaviors (WSLS), distinct from the high unconditional cooperation (ALLC) observed in Vietnamese.
