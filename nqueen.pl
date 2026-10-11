
queens(N, Qs) :-
    numlist(1, N, Rows),
    permutation(Rows, Qs),      
    safe(Qs).                   

safe([]).
safe([Q|Qs]) :-
    no_attack(Q, Qs, 1),
    safe(Qs).

no_attack(_, [], _).
no_attack(Q, [Q1|Qs], D) :-
    Q =\= Q1 + D,               
    Q =\= Q1 - D,              
    D1 is D + 1,
    no_attack(Q, Qs, D1).

print_board(Qs) :-
    length(Qs, N),
    forall(between(1, N, Row),
           ( forall(member(Q, Qs),
                    ( Q =:= Row -> write('Q ') ; write('. ') )),
             nl )).

run(N) :-
    queens(N, Qs),
    format("Solution for N = ~w: ~w~n", [N, Qs]),
    print_board(Qs),
    write("||Labno:15 || Name: Rashmin Sharma || Rollno:104/081 ||"), nl.