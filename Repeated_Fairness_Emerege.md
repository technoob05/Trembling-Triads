Emergence of Fairness in Repeated Group Interactions
S. Van Segbroeck,1 J. M. Pacheco,2,3 T. Lenaerts,1,4 and F. C. Santos5,3
1
MLG, Universite´ Libre de Bruxelles, Brussels, Belgium 2
Departamento de Matema´tica e Aplicac¸o˜es, Universidade do Minho, Braga, Portugal 3
ATP-group, CMAF, Instituto para a Investigac¸a˜o Interdisciplinar, Lisboa, Portugal 4
AI-lab, Vrije Universiteit Brussel, Brussels, Belgium 5
DEI, & INESC-ID, Instituto Superior Te´cnico, TU Lisbon, Lisboa, Portugal
(Received 26 August 2011; published 10 April 2012)
Often groups need to meet repeatedly before a decision is reached. Hence, most individual decisions
will be contingent on decisions taken previously by others. In particular, the decision to cooperate or not
will depend on one’s own assessment of what constitutes a fair group outcome. Making use of a repeated
N-person prisoner’s dilemma, we show that reciprocation towards groups opens a window of opportunity
for cooperation to thrive, leading populations to engage in dynamics involving both coordination and
coexistence, and characterized by cycles of cooperation and defection. Furthermore, we show that this
process leads to the emergence of fairness, whose level will depend on the dilemma at stake.
DOI: 10.1103/PhysRevLett.108.158104 PACS numbers: 87.23.Kg, 89.75.Fb
Many problems of cooperation among humans boil down
to the dilemma of helping others at a cost to ourselves or
refraining from doing so while still profiting from the help
provided by others [1–3]. Surprisingly often we take the
first option, even though rational considerations encourage
us not to [1,2]. This talent for cooperation forms one of the
cornerstones of human society and is, as such, also largely
responsible for the unprecedented success of our species
[4]. But how did evolution succeed in shaping such cooperative beings, if the temptation to free ride on the benefits
produced by others is always lurking? This paradox of
cooperation [5] has been under intense scrutiny for decades
and, fortunately, several mechanisms discourage us from
actually giving in to this temptation [5–15]. Physicists have
investigated some of these mechanisms (for an excellent
review, see [8]), as human cooperation constitutes an excellent example of a complex system. Cooperation may, for
instance, be worthwhile if your opponent has the chance to
return you the favor later on. If he or she is not willing to do
so, his or her cheating behavior can still be retaliated. This is
Robert Trivers’ direct reciprocity at work [16]. Theoretical
and empirical studies show that individuals who pursue
long-term relationships built on mutual cooperation are
expected to prevail [17–21]. In this context, tit-for-tat players constitute the most famous example [17]: They always
start by cooperating, subsequently repeating their opponent’s last move.
Direct reciprocation may enhance cooperation for pairwise interactions, but when larger groups of actors are
involved, decision-making becomes much more complex.
Similar to the relation between 2-body and many-body
interactions in Physics, also in human decisions there is a
significant increase in complexity when going from pairwise cooperative game interactions to collective efforts in
sizable groups. Technically, such an increase in complexity
is reflected in the number of possible behavioral equilibria,
which scales linearly with the group size [22], even in the
absence of reactive players. Moreover, it is far from clear
under which conditions a cooperator (defector) should
switch to defection (cooperation) when engaged in a repeated collective endeavor, wherein some may cooperate
while others defect. To whom should one reciprocate [23]?
One possibility is to reciprocate towards the entire group.
As in previous studies of evolution and assessment of fair
offers [24–27], reciprocating towards groups will depend
on what is reckoned as a fair collective effort, as individuals may develop an aspiration level above which they
cooperate, defecting otherwise. Such individuals constitute
a N-person generalization of the 2-person reciprocators.
Unsurprisingly, the spectrum of possible reciprocator strategies for group, N-person game interactions, is much
larger than in the 2-person case. Some reciprocators may,
for instance, be willing to cooperate only if the entire group
did so in a previous encounter, whereas others may cooperate also in the presence of group members who defected.
Let us consider group decisions involving N individuals
described in terms of the repeated N-person prisoner’s
dilemma (NPD) [28,29], in which all players have the
opportunity to contribute a certain amount c (’’cost’’) to
the public good. The accumulated amount is multiplied by
an investment factor F and subsequently shared equally
among all group members, irrespective of their contribution. This entire process repeats itself with a probability w,
resulting in an average number of hri ¼ ð1 # wÞ
#1 rounds
per group [5,30]. The outcome of the game may differ from
round to round, as individuals can base their decision to
contribute on the result of the previous round. We distinguish N different aspiration levels, encoded in terms of the
strategies RM (M 2 f1; ... ; Ng). RM players always contribute in the first round. Subsequently, they contribute
PRL 108, 158104 (2012) PHYSICAL REVIEW LETTERS week ending
13 APRIL 2012
0031-9007=12=108(15)=158104(5) 158104-1 ! 2012 American Physical Society
only if at least M players did contribute in the previous
round. The threshold M can be regarded as their own
perception of a fair number of contributions to the public
good. In addition to these N different types of reciprocators, we include the strategy AD (always defect) to account
for unconditional defectors.
Let us start by assuming an infinitely large population of
individuals, where a fraction x of the population plays
RM—allowing one single value of M in the set of all
reciprocators—while the remaining fraction plays AD.
This will allow us to define the notation before addressing
finite populations and an evolving M, while unveiling a
dynamical scenario which differs strongly from the one
obtained from (repeated) 2-person games. Behavioral dynamics often relies on individuals’ propensity to be influenced by the actions and achievements of others. Such
social learning or evolutionary dynamics can be described
by the replicator equation [31] x_ ¼ xð1 # xÞðfRM # fADÞ,
where fRM (fAD) stand for the fitness—or success—of RM
(AD) players, given by their payoff derived from the game
group interactions (see Eq. 1 in [32]).
A little algebra allows us to show that the (deterministic)
replicator dynamics leads to scenarios in which cooperation may prevail, in connection with at most two internal
fixed points, associated with unstable (coordination, x%
L)
and stable (coexistence, x%
R) equilibria, which depend on
the values of w, M, N, and F (for detailed derivations, see
Section 1 in [32]). Intuitively, the simultaneous occurrence
of these two equilibria, which happens when we face a
repeated NPD (F
 F
5 10 15 20 25 30 35 40
2.5
3.0
3.5
4.0
4.5
5.0
M*=2
M*=3
AD
(a)
(b)
M=3
M=4
M=5
AD
M=2
M=1
10-2 10-1 1
FIG. 3 (color online). Evolutionary dynamics for a) arbitrary
number of rounds and b) mutation probabilities. (a) The optimal
threshold M% as a function of F and hri in the limit of rare
mutations (w ¼ 0:9, N ¼ 5, Z ¼ 100, " ¼ 1:0). (b) Dashed
lines indicate the stationary distribution in the small-mutation
limit. Each symbol indicates, for a given mutation probability,
the fraction of the population that adopts the corresponding
strategy, averaged over the simulation time (30 simulations,
each lasting for 109 iterations; w ¼ 0:9, N ¼ 5, Z ¼ 100,
" ¼ 0:05; our results are robust to changes in " [32]).
PRL 108, 158104 (2012) PHYSICAL REVIEW LETTERS week ending
13 APRIL 2012
158104-3
over the population again (open red arrows). Hence, the
population oscillates continuously between cooperation
and defection, resembling the cycles of war and peace
similar in spirit to those identified in the context of
repeated 2-person games of cooperation [21].
This scenario constitutes a general feature of the present
model, and is not the result of a particular choice of the
average number of rounds hri (or w) or mutation probability !, as demonstrated in Fig. 3. Figure 3(a) shows that,
irrespective of the number of rounds hri, AD abounds when
F is small, RM with M ¼ 2 when F is large (but still
smaller than the group size N), and RM with M ¼ 3 for
intermediate values of F, which corresponds exactly to the
findings reported in Fig. 2(a). In other words, evolution
shapes the population assessment of fairness, depending on
the constraints imposed by the collective dilemma. In
Fig. 3(b) we investigate the robustness of our results with
respect to changes in !. We abandon the limit of rare
mutations, and determine the stationary distributions
for arbitrary mutation rates via computer simulations. For
! < Z#2, the results match the limit of rare mutations.
More importantly, the plot shows that our general conclusion remains valid for a wide range of mutation probabilities: RM players with a moderately large aspiration are
expected to prevail throughout a wide range of mutation
values. For large mutation rates (! > Z#1), all types of
reciprocators become equally probable and dominant with
respect to ADs. As a result, the overall outcome of cooperation is enhanced for high mutation rates. This is an
important point, as one expects that, e.g, in human interactions, errors of decision making, well captured by the
behavioral mutations introduced here, may be sizable [14],
although at present a quantitative estimate is lacking.
Needless to say, the results shown in Figs. 2 and 3 for
N ¼ 5, remain valid for other values of N, in the sense that
the physical order parameter of the model remains the ratio
M=N (see x! in Section 1 of [32]).
In summary, we have studied the evolutionary dynamics
of repeated group interactions, in which individuals engage
in an iterated NPD. Reciprocators are defined as individuals who may cooperate, contingent on their own individual
assessment of what constitutes a fair group contribution.
We found that evolution selects for a moderate, yet prevalent, concept of fairness in the population. This choice
results from a detailed competition between the capacity to
avoid continuous exploitation and the generosity of contributing in groups which are only partially cooperative.
The prevalent concept of fairness that emerges in the
population constitutes a compromise between too low
aspiration levels, which lead reciprocators to extinction,
and too high aspiration levels, associated with harsh
coordination thresholds. Combined with the neutrality between different concepts of fairness, the emergent dynamics leads to cyclic behavior which, being ubiquitous in
evolutionary games [8,33], also resembles the alternation
between cooperation and defection which seems to
pervade throughout human history [37].
Financial support from FNRS Belgium (S. V. S., T. L.)
and FCT-Portugal (F. C. S., J. M. P.) is gratefully
acknowledged.
[1] G. Hardin, Science 162, 1243 (1968).
[2] P. Kollock, Annu. Rev. Sociol. 24, 183 (1998).
[3] M. Olson, The Logic Of Collective Action: Public Goods
and the Theory Of Groups (Harvard University Press,
Cambridge, MA, 1971).
[4] J. Maynard Smith and E. Szathma´ry, The Major
Transitions in Evolution (Freeman, Oxford, 1995).
[5] K. Sigmund, The Calculus of Selfishness (Princeton
University Press, Princeton, NJ, 2010).
[6] F. C. Santos and J. M. Pacheco, Phys. Rev. Lett. 95,
098104 (2005).
[7] J. Go´mez-Gardenes, M. Campillo, L. M. Florı´a, and
Y. Moreno, Phys. Rev. Lett. 98, 108103 (2007).
[8] G. Szabo´, G. Fa´th, Phys. Rep. 446, 97 (2007).
[9] M. Perc and A. Szolnoki, Phys. Rev. E 77, 011904 (2008).
[10] G. Szabo´ and C. Hauert, Phys. Rev. Lett. 89, 118101
(2002).
[11] A. Traulsen, J. C. Claussen, and C. Hauert, Phys. Rev.
Lett. 95, 238701 (2005).
[12] A. Traulsen, M. A. Nowak, and J. M. Pacheco, Phys. Rev.
E 74, 011909 (2006).
[13] A. Traulsen, J. M. Pacheco, and L. A. Imhof, Phys. Rev. E
74, 021905 (2006).
[14] A. Traulsen et al., Proc. Natl. Acad. Sci. U.S.A. 106, 709
(2009).
[15] S. Van Segbroeck, F. C. Santos, T. Lenaerts, and J. M.
Pacheco, Phys. Rev. Lett. 102, 058105 (2009).
[16] R. Trivers, Q. Rev. Biol. 46, 35 (1971).
[17] R. Axelrod and W. D. Hamilton, Science 211, 1390
(1981).
[18] M. Milinski, Nature (London) 325, 433 (1987).
[19] D. Fudenberg and E. S. Maskin, Am. Econ. Rev. 80, 274
(1990).
[20] M. A. Nowak and K. Sigmund, Nature (London) 355, 250
(1992).
[21] L. A. Imhof, D. Fudenberg, and M. A. Nowak, Proc. Natl.
Acad. Sci. U.S.A. 102, 10797 (2005).
[22] C. S. Gokhale and A. Traulsen, Proc. Natl. Acad. Sci.
U.S.A. 107, 5500 (2010).
[23] K. Sigmund, Trends Ecol. Evol. 22, 593 (2007).
[24] M. Nowak, K. Page, and K. Sigmund, Science 289, 1773
(2000).
[25] J. Henrich, R. Boyd, S. Bowles, C. Camerer, H. Gintis, R.
McElreath, and E. Fehr, Am. Econ. Rev. 91, 73 (2001).
[26] K. Sigmund, E. Fehr, and M. Nowak, Sci. Am. 286, 82
(2002).
[27] J. Henrich et al., Science 327, 1480 (2010).
[28] R. Boyd and P. J. Richerson, J. Theor. Biol. 132, 337
(1988).
[29] S. Kurokawa and Y. Ihara, Proc. Biol. Sci. 276, 1379
(2009).
[30] In this setting, w and  can be used interchangeably.
PRL 108, 158104 (2012) PHYSICAL REVIEW LETTERS week ending
13 APRIL 2012
158104-4
[31] J. Hofbauer and K. Sigmund, Evolutionary Games and
Population Dynamics (Cambridge University Press,
Cambridge, England, 1998).
[32] See Supplemental Material at http://link.aps.org/
supplemental/10.1103/PhysRevLett.108.158104 for details.
[33] A. Szolnoki, M. Perc, and G. Szabo´, Phys. Rev. E 80,
056109 (2009).
[34] G. Szabo´ and C. Toke, Phys. Rev. E 58, 69 (1998).
[35] D. Fudenberg and L. Imhof, J. Econ. Theory 131, 251
(2006).
[36] In the presence of execution errors a similar result is
obtained, in which the emergent M% depends on F, w,
and the fraction of errors.
[37] P. Turchin, War and Peace and War: The Life Cycles of
Imperial Nations (Pi Press, New York, 2006).
PRL 108, 158104 (2012) PHYSICAL REVIEW LETTERS week ending
13 APRIL 2012
158104-5
Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
Supplemental Material (SM).
Supplemental Material — page 1
Supplemental Material (SM)
Emergence of Fairness in Repeated Group Interactions
Sven Van Segbroeck1, Jorge M. Pacheco2,3,
, Tom Lenaerts1,4 and Francisco C. Santos5,3
1 MLG, Université Libre de Bruxelles, Boulevard du Triomphe - CP 212, 1050 Brussels, Belgium 2 Departamento de Matemática e Aplicações, Universidade do Minho, Campus de Gualtar, 4710 - 057 Braga,
Portugal 3ATP-Group, CMAF, Complexo Interdisciplinar, P-1649-003 Lisboa Codex, Portugal 4AI-lab, Department of Computer Science, Vrije Universiteit Brussel, Pleinlaan 2, 1050 Brussels, Belgium 5 Departamento de Engenharia Informática, Instituto Superior Técnico, Universidade Técnica de Lisboa, Av.
Rovisco Pais, 1, 1049-001 Lisboa, Portugal
Summary

1. Evolutionary dynamics in infinite populations
   1.1 Overview
   1.2 Detailed analysis of Q(x)
   a. Analysis for 11. (d) Each
   curve shows the position of the roots of the fitness difference
   !
   Q(x) as a function of F for
   a particular value of M. It illustrates the dynamical scenarios pictures on the left panels,
   and is qualitatively similar to those shown in Fig. 1 of the main text (
   !
   w = 0.8, N = 5).
   Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
   Supplemental Material (SM).
   Supplemental Material — page 4
   Fig. S1 illustrates the resulting classification of the different dynamical scenarios. If
   !
   1 < M < N ,
   !
   R(x) attains a maximum at
   !
   x = "M #1
   "N #1 . Furthermore, increases
   monotonically between 0 and , and decreases monotonically between
   !
   x and 1. Then:
   (i) for , we have
   !
   Q(x) > 0, for all
   !
   x "[0,1] ; (ii) for , we have
   !
   Q(x) < 0, for all
   !
   x "[0,1] ; (iii) for
   !
   1 M < " <1 and
   !
   "r# <1+
   1$ %
   R(x )
   & r , we have
   !
   Q(x) < 0, for all
   !
   x "[0,1] ; (iv) for
   !
   1 M < " <1 and
   !
   "r# = r ,
   !
   Q(x) has a double root
   at
   !
   x = x ; (v) for
   !
   1 M < " <1 and
   !
   "r# > r ,
   !
   Q(x) has two simple roots
   !
   {xL

, xR

* },
  !
  xL
* "] 0, x [ and
  !
  xR
* "] x ,1[.
  !
  xL
* is unstable because
  !
  Q'(xL
* ) > 0,
  !
  xR
* is stable because
  !
  Q'(xR
* ) < 0.
  If M=N, our analysis consists of five cases again. The first three are exactly the same as
  for 1 r ,
  !
  Q(x) has one simple root in
  !
  x* "]0,1[.
  !
  Q(x) < 0 for
  !
  x " 0, x*
  [ [ and
  !
  Q(x) > 0 for
  !
  x " x*
  ] ,1].
  If M=1, RM is essentially the same as unconditional cooperation, making the analysis
  independent of . There are only two cases: (i) for , we have
  !
  Q(x) > 0, for all
  !
  x "[0,1] ; (ii) for
  !
  " <1, we have
  !
  Q(x) < 0, for all
  !
  x "[0,1].
  1.2. Detailed analysis of Q(x)
  In section 1.1 we sketch the evolutionary dynamics of an infinitely large, well-mixed
  population of individuals playing the repeated N-person Prisoner’s Dilemma (NPD).
  Here, we study in detail the direction of evolution by analyzing the fitness difference
  Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
  Supplemental Material (SM).
  Supplemental Material — page 5
  !
  Q(x) " fR M (x) # fAD (x). The population is in equilibrium when
  !
  Q(x) = 0. Evolution
  favors RM (AD) players if
  !
  Q(x) > 0 (
  !
  Q(x) < 0). Following Equation (1),
  !
  Q(x) equals
  !
  Q(x) = N "1
  k

$
%
&
'
(xk
(1" x)
N "k"1 )R M (k +1) " )AD ( (k))
k=0
N "1

* . (6)
  The payoff differences in this equation are given by (see Equation (2))
  !
  "R M (k +1) # "AD (k) = "AD (k +1) # "AD (k) # c(1+ (r #1)$(k +1# M)). (7)
  Note that we use r as a shorter notation for the average number of rounds
  !
  "r#. The
  payoff difference at the right-hand side of Equation (7) is given by
  , (8)
  so that Equation (7) reduces to
  . (9)
  This allows us to rewrite Equation (6) as follows
  . (10)
  Since
  , (11)
  we have that
  Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
  Supplemental Material (SM).
  Supplemental Material — page 6
  .
  (12)
  By introducing the polynomial
  , (13)
  can be written as follows
  . (14)
  In the following section, we analyze the shape of , assuming , later on
  followed by the analysis for the degenerate cases and . Together, these
  results prove the classification of all possible dynamical scenarios shown in Fig. S1.
  1.2.1. Analysis for 1 0 for
  !
  z > z and
  !
  R'(x) < 0 for
  !
  0 < z < z . The function
  !
  z = 1" x
  x
  decreases monotonously and maps
  !
  ]0,1[ on
  !
  ]0,"[. Hence, the interval
  Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
  Supplemental Material (SM).
  Supplemental Material — page 9
  !
  0 < z < z corresponds to
  !
  x < x <1. The region
  !
  z > z corresponds to
  !
  0 < x < x . This
  proves the third property of Lemma a.1. !
  Proposition a.1 Let . satisfies the following properties:

1) If , then there is a critical number of rounds which
   determines the behavior of :
   i) If , then for al .
   ii) If , then has a double root at .
   iii) If , then has two simple roots ,
   with and .
2) If , then for al .
3) If , then for al .
   Proof:
   1.i) Let . We obtain the following inequality by applying Lemma a.1
   !
   Q(x) = c(" #1) + c(r #1)R(x)
   < c(" #1) + c(r #1)R(x )
   = c(" #1) + c(r #1)
   1# "
   r #1 = 0
   , (26)
   for all
   !
   x "]0,1[. At the boundaries of the interval
   !
   [0,1], we have
   !
   Q(0) = c(" #1) < 0 and
   !
   Q(1) = cr(" #1) < 0. Hence,
   !
   Q(x) < 0 for all
   !
   x "[0,1].
   1.ii) For
   !
   r = r , we have
   !
   Q(x ) = c(" #1) + c(r #1)R(x )
   = c(" #1) + c
   1# "
   R(x )
   R(x )
   = 0
   . (27)
   Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
   Supplemental Material (SM).
   Supplemental Material — page 10
   To prove that is a double root, we show that and . The existence
   of a root in follows directly from Equation 9 and Lemma a.1:
   . To find the value of , we first derive an expression for
   . We know from Equation 18 that . The second derivative of
   is therefore given by
   . (28)
   Calculating the derivative of gives us
   . (29)
   Since , it follows that
   , (30)
   which proves that is a double root.
   1.iii) For , we have
   . (31)
   Since and , the Intermediate Value Theorem
   predicts that will have at least two roots: one root in and another root
   in . Since has only one root (see Lemma a.1), at , cannot have more
   than two roots. Hence, increases monotonically in and decreases
   monotonically in .
4) For , is positive in 0, 1, and :
   . (32)
   Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
   Supplemental Material (SM).
   Supplemental Material — page 11
   Since increases monotonically in and decreases monotonically in , it
   follows automatically that for all .
5) For , then . Therefore, decreases monotonically between 0 and 1.
   Since and , it follows that for all
   . !
   1.2.2. Analysis for M=N
   Let us derive an expression for , which is valid for , starting from Equation
   (6). By calculating the fitness differences
   (33)
   and
   , (34)
   we arrive at the following expression for :
   . (35)
   Proposition b.1 Let . satisfies the following properties:
6) If , then there is a critical number of rounds which
   determines the behavior of :
   i) If , then for al .
   ii) If , then and for al .
   Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
   Supplemental Material (SM).
   Supplemental Material — page 12
   iii) If , then has one simple root in . for
   and for .
7) If , then for al .
8) If , then for al .
   Proof: The last two properties follow directly from Equation (35). We now prove the
   first property. Note that increases monotonously if . Therefore,
   has one single root if and only if and . This condition is
   always true for . The other condition, , holds in case .
   !
   1.2.3. Analysis for M=1
   For M=1, Equation (4) reduces to
   !
   "R M (k +1) # "AD (k) = ($ #1)cr. (36)
   Therefore,
   , (37)
   which proves the proposition below.
   Proposition c.1 Let M=1. Q(x) satisfies the following properties:
9) If , then for al .
10) If , then for al .
    Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
    Supplemental Material (SM).
    Supplemental Material — page 13

2. Evolutionary dynamics in finite populations
   2.1. Overview
   We consider a well-mixed population of constant size Z. Suppose that only two
   strategies are present in the population: AD and RM, M being fixed at one specific value.
   The expected payoff associated with each of these two strategies is given by [3, 4]
   , (38)
   where k denotes the number of RM players in the population.
   Strategies evolve according to a mutation-selection process defined in discrete time. At
   each time step, the strategy of one randomly selected individual A is updated. With
   probability , A undergoes a mutation. He/she adopts a strategy drawn randomly from
   the space of available strategies, which includes the strategy AD and the N strategies RM
   ( ). With probability , another randomly selected individual B acts as a
   role model for A. The probability that A adopts the strategy of B
   equals
   !
   p = 1+ e" ( fA # fB ) [ ]
   #1
   . A sticks to his/her former strategy with probability .
   This update rule is known as the pairwise comparison rule [6, 7]. We used fA and fB to
   denote the fitness of individual A and B, respectively. The parameter , in EGT
   called the intensity of selection, measures the contribution of fitness to the update
   process. In the limit of strong selection ( ), the probability p is either zero or one,
   depending on fA and fB. In the limit of weak selection ( ), p is always equal to ,
   irrespective of the fitness of A and B.
   If the mutation probability is sufficiently small, the population will never contain
   Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
   Supplemental Material (SM).
   Supplemental Material — page 14
   more than two different strategies simultaneously. The time between two mutation
   events is usually so large that the population will always evolve to a homogeneous state,
   i.e., to a state in which all individuals adopt the same strategy, before the next mutation
   occurs. The dynamics can now be approximated by means of an embedded Markov
   chain whose states correspond to the different homogeneous states of the population [8-
   11]. Let us denote the list of available strategies as Si ( ). The transition
   matrix collects the different (transition) probabilities for the
   population to move from one state to the other. Specifically, is the probability that a
   population in state Si will end up in state Sj after the occurrence of one single mutation.
   This probability is given by , where is the probability that a Sj
   mutant takes over a resident population of Si individuals. The diagonal of the transition
   matrix is defined by . The normalized left eigenvector associated
   with eigenvalue 1 of matrix determines the stationary distribution, i.e, the fraction of
   time the population spends in each of the homogeneous states of the population [12,
   13].
   The fixation probability can be calculated analytically as follows. Let us assume a
   population with k Si individuals and Z-k Sj individuals. The probability that the number
   of Si individuals increases/decreases by one is given by
   , (39)
   establishing also the probability [6, 7, 14]
   . (40).
   Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
   Supplemental Material (SM).
   Supplemental Material — page 15
   Finally, it is important to highlight the difference between behavioural mutations and
   execution or implementation errors. In this context, the latter turns the analytical
   computation of the fitness values of each strategy cumbersome (see Eqs. (2) and (38)),
   being however easy to compute numerically. In fact, all results portrayed in Fig. 2 of the
   main text remain qualitatively unaltered if one adopts a small probability (!) associated
   with a limited fraction of implementation errors.
   2.2. Computer simulations
   All individual-based computer simulations start from a randomly initialized population
   of size . The population dynamics is implemented following the rules described
   above. We calculate the fitness of an individual by averaging the payoff he/she acquires
   in 1000 NPD’s with randomly selected partners. We have checked that the obtained
   values provide a good approximation of the actual expected payoff values, which are
   given by Equation (38) in case of just two strategies. The stationary distributions shown
   in Fig. 3 of the main text are computed as the configuration of the population averaged
   over the entire simulation time (109
   iterations). We do 30 independent runs for each
   value of . The value of !=0.05 reflects a convenient choice in terms of computation
   time, but similar results are obtained if we adopt the selection of strength (!=1.0) used
   in the rest of the figures (see stationary distributions in Fig. 2 and dashed lines in Fig.
   3b).
3. References
   [1] J. Hofbauer, and K. Sigmund, Evolutionary Games and Population Dynamics
   (Cambridge University Press, Cambridge, UK, 1998).
   [2] K. Sigmund, The Calculus of Selfishness (Princeton University Press, 2010).
   [3] C. Hauert et al., Journal of Theoretical Biology 239, 195 (2006).
   [4] J. M. Pacheco et al., Proc. R. Soc. B 276, 315 (2008).
   [5] C. S. Gokhale, and A. Traulsen, Proc Natl Acad Sci U S A 107, 5500 (2010).
   Van Segbroeck, Pacheco, Lenaerts and Santos, Emergence of fairness in repeated group interactions,
   Supplemental Material (SM).
   Supplemental Material — page 16
   [6] A. Traulsen, J. M. Pacheco, and M. A. Nowak, J Theor Biol 246, 522 (2007).
   [7] A. Traulsen, M. A. Nowak, and J. M. Pacheco, Phys Rev E 74 011090 (2006).
   [8] D. Fudenberg, and L. Imhof, J Econ Theory 131, 251 (2005).
   [9] L. A. Imhof, D. Fudenberg, and M. A. Nowak, Proc Natl Acad Sci U S A 102,
   10797 (2005).
   [10] C. Hauert et al., Science 316, 1905 (2007).
   [11] S. Van Segbroeck et al., Phys Rev Lett 102, 58105 (2009).
   [12] S. Karlin, and H. E. Taylor, A First Course in Stochastic Processes (Academic
   Press, 1975).
   [13] N. G. Van Kampen, Stochastic Processes in Physics and Chemistry (North
   Holland, 2007).
   [14] A. Traulsen, N. Shoresh, and M. A. Nowak, Bull Math Biol 70, 1410 (2008).
