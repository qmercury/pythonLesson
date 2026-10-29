"""03 | 좌표 목록을 차례로 연결해 집 모양을 그려요."""
import turtle

screen = turtle.Screen()
screen.title("03 - Coordinate Drawing")
pen = turtle.Turtle()
pen.speed(4)
pen.pensize(3)

house = [(-90, -100), (90, -100), (90, 30),
         (0, 110), (-90, 30), (-90, -100)]
pen.penup()
pen.goto(house[0])
pen.pendown()
for x, y in house[1:]:
    pen.goto(x, y)

pen.penup()
pen.goto(-20, -100)
pen.pendown()
for x, y in [(-20, -25), (20, -25), (20, -100)]:
    pen.goto(x, y)

pen.hideturtle()
screen.mainloop()
