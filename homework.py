class InfoMessage:
    """Info message about training."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return str(f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Base class of training."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029
    min_in_hour: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get average speed."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Get burned calories."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Get back info message about training."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Training: run."""

    def get_spent_calories(self) -> float:
        calories = (self.coeff_calorie_1 * self.get_mean_speed() -
                    self.coeff_calorie_2) * self.weight / self.M_IN_KM \
                   * (self.duration * self.min_in_hour)
        return calories


class SportsWalking(Training):
    """Training: sports walking."""

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.coeff_calorie_3 * self.weight +
                     ((self.get_mean_speed() ** 2) // self.height) *
                     self.coeff_calorie_4 * self.weight) *
                    (self.duration * self.min_in_hour))
        return calories


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38

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
        """Get distance in swimmingpool in km."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get average speed in swimmingpool."""
        speed = \
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Read sensor data."""
    dict_tr = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    class_name = dict_tr.get(workout_type)
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
