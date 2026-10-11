hanoi(0, _, _, _) :- !.                    
hanoi(N, Source, Target, Auxiliary) :-
    N > 0,
    N1 is N - 1,
    hanoi(N1, Source, Auxiliary, Target),  
    move(N, Source, Target),               
    hanoi(N1, Auxiliary, Target, Source).  

move(Disk, From, To) :-
    format("Move disk ~w from ~w to ~w~n", [Disk, From, To]).

hanoi_moves(0, 0) :- !.
hanoi_moves(N, Moves) :-
    N1 is N - 1,
    hanoi_moves(N1, M1),
    Moves is 2 * M1 + 1.
    
run(N) :-
    format("Tower of Hanoi with ~w disk(s):~n", [N]),
    hanoi(N, left, right, center),
    hanoi_moves(N, Moves),
    format("Total moves: ~w~n", [Moves]),
    write("||Labno: 18 || Name: Rashmin Sharma || Rollno:104/081 ||"), nl.