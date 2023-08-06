import torch
from pytorch_memlab import profile


@profile
def func1():

    inp = torch.randn(100, 100).cuda()
    net = torch.nn.Linear(100, 100).cuda()
    for _ in range(2):
        out = net(inp)
        func2()

@profile
def func2():
    inp = torch.randn(100, 100).cuda()
    net = torch.nn.Linear(100, 100).cuda()
    for _ in range(2):
        out = net(inp)

func1()
