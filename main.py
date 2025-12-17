import arcade
import GameManager

def main():
    game = GameManager.Limbo()
    game.setup(0)  # Начинаем с первого уровня
    arcade.run()


if __name__ == "__main__":
    main()