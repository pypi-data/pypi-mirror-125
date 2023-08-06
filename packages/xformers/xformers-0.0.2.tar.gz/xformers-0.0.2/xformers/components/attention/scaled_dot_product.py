# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
#
# This source code is licensed under the BSD license found in the
# LICENSE file in the root directory of this source tree.

from typing import Optional

import torch
from torch import nn

from xformers.components.attention import Attention, AttentionConfig, register_attention
from xformers.components.attention.core import scaled_dot_product_attention


@register_attention("scaled_dot_product", AttentionConfig)
class ScaledDotProduct(Attention):
    r"""
    Implementing the Scaled Dot-Product attention proposed in
    `Attention is all you need`_, Vaswani et al.

    .. _`Attention is all you need`: https://arxiv.org/abs/1706.03762v5
    """

    mask: Optional[torch.Tensor]

    def __init__(
        self,
        dropout: float = 0.0,
        causal: bool = False,
        seq_len: Optional[int] = None,
        to_seq_len: Optional[int] = None,
        *args,
        **kwargs,
    ):
        super().__init__()
        self.attn_drop = nn.Dropout(dropout, inplace=False)
        self.causal = causal
        self.seq_len = seq_len

        if causal and seq_len is not None:
            mask = self._get_causal_mask(seq_len, to_seq_len if to_seq_len else seq_len)
            self.register_buffer("mask", mask)
        else:
            self.mask = None

    def forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        att_mask: Optional[torch.Tensor] = None,
        *args,
        **kwargs,
    ) -> torch.Tensor:
        r"""
        att_mask    A 2D or 3D mask which ignores attention at certain positions. A value of True will keep the
                    value, while a value of False will mask the value. Key padding masks
                    (dimension: batch x sequence length) and attention masks
                    (dimension: sequence length x sequence length OR batch x sequence length x sequence length)
                    can be combined and passed in here. Method maybe_merge_masks provided in the utils can be
                    used for that merging. Additive masks are not yet supported.
        """
        # Mask-aware attention
        if self.mask is not None:
            att_mask = self.mask if att_mask is None else self.mask & att_mask

        # Self-attend: (B x nh, S, hs) x (B x nh, hs, S) -> (B x nh, S, S)
        y = scaled_dot_product_attention(
            q=q, k=k, v=v, att_mask=att_mask, dropout=self.attn_drop, causal=self.causal
        )
        return y
