
instance_of(subhash, student).
instance_of(ram, player).

subclass_of(student, person).
subclass_of(game, physical_action).

has(person, hair).
plays(player, game).
height_larger_than(player, student).
starts_at(physical_action, '7am').
ends_at(physical_action, '9am').


subclass_star(C, C).
subclass_star(C, D) :- subclass_of(C, E), subclass_star(E, D).


member_of(X, C) :- instance_of(X, C0), subclass_star(C0, C).


has_property(X, P) :- member_of(X, C), has(C, P).


plays_game(X, G) :- member_of(X, C), plays(C, G).

start_time(A, T) :- subclass_star(A, C), starts_at(C, T).
end_time(A, T)   :- subclass_star(A, C), ends_at(C, T).


taller(X, Y) :-
    member_of(X, CX),
    member_of(Y, CY),
    height_larger_than(CX, CY).


yn(Goal) :- ( call(Goal) -> writeln(yes) ; writeln(no) ).

run :-
    write("Is Subhash taller than Ram?   "), yn(taller(subhash, ram)),
    write("Is Ram taller than Subhash?   "), yn(taller(ram, subhash)),
    write("Is Subhash a person?          "), yn(member_of(subhash, person)),
    write("Does Subhash have hair?       "), yn(has_property(subhash, hair)),
    write("Does Ram play a game?         "), yn(plays_game(ram, game)),
    ( start_time(game, S), end_time(game, E)
    -> format("Game starts at ~w and ends at ~w~n", [S, E]) ; true ),
    write("||Labno: 20 || Name: Rashmin Sharma || Rollno:104/081 ||"), nl.