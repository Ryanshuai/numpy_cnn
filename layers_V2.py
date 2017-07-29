import numpy as np
from im2col import im2col
from im2col import col2im

class conv2d():
    def __init__(self, input_size, filter_size, strides, padding='valid'):
        self.BS, self.in_H, self.in_W, self.in_D = input_size #[batch，高，宽，通道数]
        self.f_H, self.f_W, _, self.out_D = filter_size #[高，宽，输入通道数，输出通道数]
        self.stride_H, self.stride_W = strides #[高上步长，宽上步长]
        self.pad_H ,self.pad_W = 0, 0
        if padding == 'same':
            self.pad_H = (self.f_H-1)/2
            self.pad_W = (self.f_W-1)/2
        self.out_H = int((self.in_H - self.f_H + 2*self.pad_H)/self.stride_H + 1)
        self.out_W = int((self.in_W - self.f_W + 2*self.pad_W)/self.stride_W + 1)

        Weight = []
        self.W_col = Weight.reshape(self.out_D,-1) #shape=(out_D,f_H*f_W*in_D)
        self.b = 0.*np.ones((self.out_D, 1), dtype=np.float32)


    def forward_propagate(self,X):
        X_col = im2col(X, self.f_H, self.f_W, pad=[self.pad_H,self.pad_W], stride=[self.stride_H, self.stride_W])#shape=(f_H*f_W*in_D,out_H*out_W*BS)
        out = np.matmul(self.W_col, X_col) + self.b #shape=(out_D,out_H*out_W*BS)
        out = out.reshape(self.out_D,self.out_H,self.out_W,self.BS) #shape=(out_D,out_H*out_W*BS)->(out_D,out_H,out_W,BS)
        out = out.transpose(3,0,1,2)
        return out

    def back_propagate(self):
        pass
