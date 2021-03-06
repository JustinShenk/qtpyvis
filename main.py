#!/usr/bin/env python

import sys
import argparse
import numpy as np

from PyQt5.QtWidgets import QApplication

from qtgui.main import DeepVisMainWindow
#from list_of_funnctions import KerasNetwork
from network import KerasTensorFlowNetwork
from network import TorchNetwork

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Neural network analysis.')
    parser.add_argument("--model", help = 'filename of model to use',
                        default = 'models/example_keras_mnist_model.h5')
    parser.add_argument("--data", help = 'filename of dataset to visualize',
                        default = 'mnist')
    parser.add_argument("--framework", help = 'the framework to use '
                        '(keras-tensorflow, torch)',
                        default = 'keras-tensorflow')
    args = parser.parse_args()

    if args.framework == 'keras-tensorflow':
        #network = KerasNetwork(args.model)
        if not args.model:
            args.model = 'models/example_keras_mnist_model.h5'
        network = KerasTensorFlowNetwork(model_file=args.model)
    elif args.framework == 'torch':
        # FIXME[hack]: provide these parameter on the command line ...
        net_file = "models/example_torch_mnist_net.py"
        net_class = "Net"
        parameter_file = "models/example_torch_mnist_model.pth"
        input_shape = (28,28)
        network = TorchNetwork(net_file, parameter_file,
                               net_class = net_class,
                               input_shape = input_shape)

    if args.data=='mnist':
        from keras.datasets import mnist
        data = mnist.load_data()[0][0]
    else:
        data = np.load(args.data)

    data = data.reshape(data.shape[0],data.shape[1],data.shape[2],1)

    app = QApplication(sys.argv)
    mainWindow = DeepVisMainWindow()
    mainWindow.setNetwork(network, data)
    mainWindow.show()

    rc = app.exec_()
    print("Good bye ({})".format(rc))
    sys.exit(rc)
