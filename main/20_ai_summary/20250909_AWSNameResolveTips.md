---
title: "AWSを利用する上で知っておきたい名前解決のはなし（10分版）"
source: "https://speakerdeck.com/nagisa53/awswoli-yong-surushang-dezhi-tuteokitaiming-qian-jie-jue-nohanasi-10fen-ban"
author:
  - "[[nagisa_53]]"
published: 2025-09-09
created: 2025-11-17
description: "AWS名前解決の3分類と落とし穴"
tags:
  - "ai_summary"
  - "dns"
  - "networking"
  - "aws"
  - "resilience"
---
## Key Points
- AWSリソースの名前解決を①パブリックDNS→グローバルIP、②パブリックDNS→プライベートIP、③VPC内限定に分類し、CloudFront/NLB/EFSなどの該当サービスを整理。
- ②のケースでは同一VPCやTransit Gateway配下のみ疎通でき、カスタムドメインやTLS証明書の要件で③へ寄せる必要があることを解説。
- ③のVPC内解決はRoute 53 Resolver Inbound Endpoint等を使えばオンプレや別VPCから引けるという構成例を紹介。
- VPC LatticeやInterface型エンドポイントのプライベートDNS設定によって返るIP/疎通範囲が変わる例、リンクローカル返却など特殊ケースも扱う。
- NLBなど「IP固定」のサービスでも障害時に入れ替わる可能性があり、TTL順守とキャッシュ設計が重要だと強調。
## 運用メモ
- DNSのどこで解決され何が返るかを図解して共有することで、トラブルシューティングが速くなるというメッセージが刺さる。
