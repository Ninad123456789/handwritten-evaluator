import numpy as np
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense


class HES_Model:
    def __init__(self, weights='weights.hdf5'):
        self.model = None
        self.weights = weights
        self.chars = ['*', '+', '-', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')']
        self.initialize_model()

    def initialize_model(self):
        self.model = Sequential()
        self.model.add(Conv2D(30, (5, 5), input_shape=(28, 28, 1), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(15, (5, 5), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.3))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(16, activation='softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
        self.model.load_weights(self.weights)

    def predict_equation(self, image_list):
        for i in range(len(image_list)):
            # Converting it to array
            image_list[i] = image.img_to_array(image_list[i])
            # Normalizing the pixel value
            image_list[i] = image_list[i] / 225

        image_list = np.array(image_list)
        predictions = np.argmax(self.model.predict(image_list), axis=-1)

        equation = ''
        for i in predictions:
            equation += self.chars[i]
        return equation


def precedence(operator):
    if operator in ['*', '/']:
        return 2
    if operator in ['+', '-']:
        return 1
    return 0


def apply_operation(a, b, operator):
    a = float(a)
    b = float(b)

    if operator == '/':
        return a / b
    if operator == '*':
        return a * b
    if operator == '+':
        return a + b
    if operator == '-':
        return a - b


def evaluate(equation):
    operators = []
    operands = []
    i = 0

    # noinspection PyBroadException
    try:
        while i < len(equation):

            if equation[i] == ' ':
                i += 1
                continue

            elif equation[i] == '(':
                operands.append(equation[i])

            elif equation[i].isdigit():
                val = 0
                while (i < len(equation) and
                       equation[i].isdigit()):
                    val = (val * 10) + int(equation[i])
                    i += 1
                operators.append(val)
                i -= 1

            elif equation[i] == ')':
                while len(operands) != 0 and operands[-1] != '(':
                    val2 = operators.pop()
                    val1 = operators.pop()
                    op = operands.pop()
                    operators.append(apply_operation(val1, val2, op))
                operands.pop()

            else:
                while len(operands) != 0 and precedence(operands[-1]) >= precedence(equation[i]):
                    val2 = operators.pop()
                    val1 = operators.pop()
                    op = operands.pop()
                    operators.append(apply_operation(val1, val2, op))
                operands.append(equation[i])

            i += 1

        while len(operands) != 0:
            val2 = operators.pop()
            val1 = operators.pop()
            op = operands.pop()
            operators.append(apply_operation(val1, val2, op))

        return round(operators[-1], 4)
    except ZeroDivisionError:
        return 'Error : Can not divide by zero.'
    except Exception:
        return 'Error : Invalid expression.'
