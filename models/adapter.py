from torch import nn
import torch.nn.functional as F

from models.gpdl import generation_init_weights


class Adapter(nn.Module):
    # embed_dim：输入/输出
    def __init__(self, adapter_dim, embed_dim):
        super(Adapter, self).__init__()
        self.group_norm = nn.GroupNorm(num_groups=1, num_channels=embed_dim)  # num_groups=1 等价于 LayerNorm
        self.down_project = nn.Conv2d(embed_dim, adapter_dim, kernel_size=1, bias=False)  # 使用 1x1 卷积
        # self.middle_project = nn.Conv2d(adapter_dim, adapter_dim, kernel_size=3, padding=1, bias=False)
        self.up_project = nn.Conv2d(adapter_dim, embed_dim, kernel_size=1, bias=False)  # 使用 1x1 卷积

    def forward(self, z):
        normalized_z = self.group_norm(z)
        h = F.leaky_relu(self.down_project(normalized_z), 0.2, inplace=True)
        # h = F.leaky_relu(self.middle_project(h), 0.2, inplace=True)
        return self.up_project(h) + z

    def init_weights(self):
        generation_init_weights(self)