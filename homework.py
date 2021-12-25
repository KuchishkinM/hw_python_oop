from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Generates a message about training."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return str('Тип тренировки: {0}; '
                   'Длительность: {1:.3f} ч.; '
                   'Дистанция: {2:.3f} км; '
                   'Ср. скорость: {3:.3f} км/ч; '
                   'Потрачено ккал: {4:.3f}.').format(self.training_type,
                                                      self.duration,
                                                      self.distance,
                                                      self.speed,
                                                      self.calories
                                                      )


class Training:
    """Base class of training."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Calculates distance in km. based on action and two constants."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Calculates average speed in km/hour based on duration and
        distance."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Calculates the number of calories burned in a workout
        based on the type of workout"""
        pass

    def show_training_info(self) -> InfoMessage:
        """Get back info message about training."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Training: run."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                     - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                    * (self.duration * self.MIN_IN_HOUR))
        #        run_step_1 = ((self.COEFF_CALORIE_1 * self.get_mean_speed())
        #                      - self.COEFF_CALORIE_2)
        #       run_step_2 = self.weight / self.M_IN_KM
        #       run_step_3 = self.duration * self.MIN_IN_HOUR
        #        calories = run_step_1 * run_step_2 * run_step_3
        # Тут пытался разбить формулу, как ты просил, но как я ее только не
        # разбивал, тесты проходить не хочет(((
        return calories


class SportsWalking(Training):
    """Training: sports walking."""
    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        walk_step_1 = (self.get_mean_speed() ** 2) // self.height
        walk_step_2 = (self.COEFF_CALORIE_3 * self.weight + walk_step_1
                       * self.COEFF_CALORIE_4 * self.weight)
        calories = walk_step_2 * (self.duration * self.MIN_IN_HOUR)
        return calories


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38
    SUPER_1_1: float = 1.1
    ALL_LOVE_TWO: float = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Calculates distance in swimmingpool based on action and two
        constants."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Calculates average speed in swimmingpool based on duration and three
        constants."""
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        swimm_step_1 = self.get_mean_speed() + self.SUPER_1_1
        calories = swimm_step_1 * self.ALL_LOVE_TWO * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Reads data from sensors and converts them into a dictionary."""
    training_name: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    class_name = training_name.get(workout_type)
    return class_name(*data)


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
