from pop_corn.matrix import Matrix, Vec

class Perceptron:
    def __init__(self, name_or_input_size, output_size=None):
        if isinstance(name_or_input_size,str):
            self.weights = Matrix.load_file(name_or_input_size)
        else:
            self.weights = Matrix(name_or_input_size+1, output_size+1,  [random.random() for _ in range((name_or_input_size+1) * (output_size+1))])  

    def predict(self, inputs):
        tail=False
        if inputs.n==self.weights.m-1:
            result = Matrix.untail(Matrix.tail(inputs) * self.weights)
        else:
            result = inputs * self.weights
        return result

    def train(self, inputs, labels, learning_rate=0.01, epochs=1):
#         if inputs.n==self.weights.m-1:
#             inputs=Matrix.tail(inputs)
#         if labels.n==self.weights.n-1:
#             labels=Matrix.tail(labels)
        for epoch in range(epochs):
            predictions = self.predict(inputs)
            error = labels - predictions
#            self.weights=self.weights.add_tail(  inputs.T() * error * learning_rate)
            self.weights=  inputs.T() @ error * learning_rate
            
    def save_file(self,name):
        self.weights.save_file(name)
