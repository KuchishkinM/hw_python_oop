from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Type


@dataclass
class InfoMessage:
    """Generates a message about training."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    TEMPLATE_INFO: str = ('Тип тренировки: {training_type}; '
                          'Длительность: {duration:.3f} ч.; '
                          'Дистанция: {distance:.3f} км; '
                          'Ср. скорость: {speed:.3f} км/ч; '
                          'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.TEMPLATE_INFO.format(**asdict(self))


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
        raise NotImplementedError('Define get_spent_calories!!!')

    def show_training_info(self) -> InfoMessage:
        """Get back info message about training."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Training: run."""
    RUN_COEFF_CALORIE_1: float = 18
    RUN_COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        speed_with_coeff = (self.RUN_COEFF_CALORIE_1 * self.get_mean_speed()
                            - self.RUN_COEFF_CALORIE_2) * self.weight
        duration_minutes = self.duration * self.MIN_IN_HOUR
        calories = speed_with_coeff / self.M_IN_KM * duration_minutes
        return calories


class SportsWalking(Training):
    """Training: sports walking."""
    WLK_COEFF_CALORIE_1: float = 0.035
    WLK_COEFF_CALORIE_2: float = 0.029
    WLK_COEFF_CALORIE_3: float = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        weight_with_coeff_1 = self.WLK_COEFF_CALORIE_1 * self.weight
        weight_with_coeff_2 = self.WLK_COEFF_CALORIE_2 * self.weight
        mean_speed_with_weight = ((self.get_mean_speed()
                                   ** self.WLK_COEFF_CALORIE_3)
                                  // self.height)
        duration_minutes = self.duration * self.MIN_IN_HOUR
        calories = ((weight_with_coeff_1 + mean_speed_with_weight
                     * weight_with_coeff_2) * duration_minutes)
        return calories


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38
    SWM_COEFF_CALORIE_1: float = 1.1
    SWM_COEFF_CALORIE_2: float = 2

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
        distance_meters = self.length_pool * self.count_pool
        distance_km = distance_meters / self.M_IN_KM
        speed = distance_km / self.duration
        return speed

    def get_spent_calories(self) -> float:
        mean_speed_with_coeff = self.get_mean_speed() + self.SWM_COEFF_CALORIE_1
        calories = (mean_speed_with_coeff * self.SWM_COEFF_CALORIE_2
                    * self.weight)
        return calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Reads data from sensors and converts them into a dictionary."""
    training_name: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_name:
        raise ValueError(f'Sorry, but {workout_type} wrong name WORKOUT_TYPE. '
                         'Try to use one of: (SWM, RUN, WLK)')
    return training_name[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
