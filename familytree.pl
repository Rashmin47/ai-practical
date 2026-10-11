
male(george).  male(john).   male(peter).  male(robert).
male(david).   male(tom).    male(james).

female(mary).  female(linda). female(susan). female(anna).
female(sophie). female(emma). female(kate).  female(lily).

parent(george, john).   parent(mary, john).
parent(george, susan).  parent(mary, susan).
parent(george, peter).  parent(mary, peter).

parent(john, david).    parent(linda, david).
parent(john, emma).     parent(linda, emma).

parent(susan, kate).    parent(robert, kate).
parent(susan, tom).     parent(robert, tom).

parent(peter, james).   parent(anna, james).

parent(david, lily).    parent(sophie, lily).

father(F, C)  :- parent(F, C), male(F).
mother(M, C)  :- parent(M, C), female(M).

son(S, P)       :- parent(P, S), male(S).
daughter(D, P)  :- parent(P, D), female(D).

sibling(X, Y) :- parent(P, X), parent(P, Y), X \== Y.
brother(B, X) :- sibling(B, X), male(B).
sister(S, X)  :- sibling(S, X), female(S).

grandparent(G, C) :- parent(G, P), parent(P, C).
grandfather(G, C) :- grandparent(G, C), male(G).
grandmother(G, C) :- grandparent(G, C), female(G).
grandchild(C, G)  :- grandparent(G, C).

uncle(U, X) :- parent(P, X), brother(U, P).
aunt(A, X)  :- parent(P, X), sister(A, P).

cousin(X, Y) :- parent(P1, X), parent(P2, Y), sibling(P1, P2).

ancestor(A, X) :- parent(A, X).
ancestor(A, X) :- parent(P, X), ancestor(A, P).
descendant(D, A) :- ancestor(A, D).

all(Goal, Var) :-
    setof(Var, Goal, List),
    format("~w~n", [List]).
all(_, _) :- writeln([]).       

run :-
    write("Father of david:        "), all(father(F, david), F),
    write("Mother of kate:         "), all(mother(M, kate), M),
    write("Siblings of david:      "), all(sibling(S, david), S),
    write("Brothers of kate:       "), all(brother(B, kate), B),
    write("Grandparents of lily:   "), all(grandparent(G, lily), G),
    write("Grandchildren of mary:  "), all(grandchild(C, mary), C),
    write("Uncles of david:        "), all(uncle(U, david), U),
    write("Aunts of david:         "), all(aunt(A, david), A),
    write("Cousins of david:       "), all(cousin(X, david), X),
    write("Ancestors of lily:      "), all(ancestor(A2, lily), A2),
    write("Descendants of george:  "), all(descendant(D, george), D),
    write("||Labno: 17 || Name: Rashmin Sharma || Rollno:104/081 ||"), nl.