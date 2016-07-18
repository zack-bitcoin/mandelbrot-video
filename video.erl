-module(video).
-export([main/0,draw/1]).

-define(focusr, 0.3507069).
-define(focusi, 0.4259650595).
-define(initial_zoom, 900).
%-define(initial_zoom, 400).
-define(initial_width, 0.35).
-define(step, 1.7320508075688772).
%-define(steps, 32).
-define(steps, 37).

main() -> draw_all(1, ?steps).
draw_all(X, Y) when X>Y -> ok;
draw_all(X, Y) ->
    os:cmd(draw(X)),
    draw_all(X+1, Y).

float_to_string(F) -> hd(io_lib:format("~.10f", [abs(F)])).
draw(StepNumber) ->
    %initial width is 3, always decreasing from there.
    io:fwrite("draw: "),
    io:fwrite(integer_to_list(StepNumber)),
    io:fwrite("\n"),
    R = math:pow(?step, StepNumber),
    Z = ?initial_zoom * R,
    W = ?initial_width / R,
    "./mandelbrotG5.py -r "++float_to_string(?focusr-(W*8/5))++","++ float_to_string(?focusr+(W*8/5))++" -I "++float_to_string(?focusi-W)++","++float_to_string(?focusi+W)++" -z "++integer_to_list(round(Z)) ++ " -o " ++ "image" ++ string:right(integer_to_list(StepNumber), 2, $0).


%os:cmd("./mandelbrotG5.py -r 0.350705,0.350715 -I 0.425965,0.425975 -z 20000000").
