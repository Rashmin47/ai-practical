
position(middle).      
position(atdoor).
position(atwindow).


move(state(middle, onbox, middle, hasnot),
     grasp,
     state(middle, onbox, middle, has)).

move(state(P, onfloor, P, H),
     climb,
     state(P, onbox, P, H)).

move(state(P1, onfloor, P1, H),
     push(P1, P2),
     state(P2, onfloor, P2, H)) :-
    position(P2), P1 \== P2.

move(state(P1, onfloor, B, H),
     walk(P1, P2),
     state(P2, onfloor, B, H)) :-
    position(P2), P1 \== P2.

canget(State, Plan) :-
    canget(State, [State], Plan).

canget(state(_, _, _, has), _, []).                 
canget(State1, Visited, [Action|Actions]) :-
    move(State1, Action, State2),
    \+ member(State2, Visited),                    
    canget(State2, [State2|Visited], Actions).

run :-
    Start = state(atdoor, onfloor, atwindow, hasnot),
    format("Initial state: ~w~n", [Start]),
    findall(P, canget(Start, P), Plans),            
    length(Plans, Count),
    format("Number of different plans: ~w~n", [Count]),
    shortest(Plans, Plan),
    format("Shortest plan: ~w~n", [Plan]),
    print_steps(Plan, 1),
    write("||Labno: 16 || Name: Rashmin Sharma || Rollno:104/081"), nl.


print_steps([], _).
print_steps([A|As], N) :-
    format("  Step ~w: ~w~n", [N, A]),
    N1 is N + 1,
    print_steps(As, N1).

shortest([P|Ps], Best) :- shortest(Ps, P, Best).
shortest([], Best, Best).
shortest([P|Ps], Cur, Best) :-
    length(P, L), length(Cur, LC),
    ( L < LC -> shortest(Ps, P, Best) ; shortest(Ps, Cur, Best) ).