
immortal :- mythical.                 

mortal   :- \+ mythical.               
mammal   :- \+ mythical.              

horned :- immortal.                    
horned :- mammal.

magical :- horned.                    

yes_no(Goal, Answer) :- ( call(Goal) -> Answer = yes ; Answer = no ).

report :-
    forall(member(P, [mythical, immortal, mortal, mammal, horned, magical]),
           ( yes_no(P, A), format("  ~w? ~w~n", [P, A]) )).


run :-
    retractall(mythical),
    writeln("Case 1: the unicorn is NOT mythical"),
    report,
    assertz(mythical),
    writeln("Case 2: the unicorn IS mythical"),
    report,
    retractall(mythical),
    writeln("Conclusion: in both cases the unicorn is horned and magical;"),
    writeln("whether it is mythical cannot be decided from the sentences."),
    write("||Labno: 19 || Name: Rashmin Sharma || Rollno:104/081 ||"), nl.