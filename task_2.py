"""Draw Koch snowflake recursively using Python's standard turtle module."""
import turtle


def koch_segment(pen: turtle.Turtle, length: float, depth: int) -> None:
    if depth == 0:
        pen.forward(length)
        return
    part = length / 3
    koch_segment(pen, part, depth - 1)
    pen.left(60)
    koch_segment(pen, part, depth - 1)
    pen.right(120)
    koch_segment(pen, part, depth - 1)
    pen.left(60)
    koch_segment(pen, part, depth - 1)


def draw_snowflake(depth: int) -> None:
    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха — рівень {depth}")
    screen.setup(width=950, height=800)
    screen.tracer(0, 0)
    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.pensize(2)
    length = 420
    pen.penup()
    pen.goto(-length / 2, length / 3)
    pen.pendown()
    for _ in range(3):
        koch_segment(pen, length, depth)
        pen.right(120)
    screen.update()
    screen.mainloop()


def main() -> None:
    while True:
        try:
            depth = int(input('Введіть рівень рекурсії (0–5): '))
            if 0 <= depth <= 5:
                break
            print('Введіть ціле число від 0 до 5.')
        except ValueError:
            print('Потрібно ввести ціле число.')
    draw_snowflake(depth)


if __name__ == '__main__':
    main()
