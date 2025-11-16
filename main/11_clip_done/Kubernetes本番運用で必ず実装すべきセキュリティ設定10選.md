---
title: "Kubernetes本番運用で必ず実装すべきセキュリティ設定10選"
source: "https://qiita.com/keitah/items/c25440de24eea858a24b?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share"
author:
  - "[[keitah]]"
published: 2025-10-16
created: 2025-11-17
description: "はじめに Kubernetesは現代のクラウドネイティブアプリケーション基盤として広く採用されていますが、その複雑さゆえにセキュリティの設定ミスが多発しています。 衝撃的な統計データ（2025年）: テストされた全クラウド環境の**100%**に少なくとも1つの設定ミス..."
tags:
  - "clippings"
  - raw
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=217143)

## はじめに

Kubernetesは現代のクラウドネイティブアプリケーション基盤として広く採用されていますが、その複雑さゆえにセキュリティの設定ミスが多発しています。

**衝撃的な統計データ（2025年）:**

- テストされた全クラウド環境の\*\*100%\*\*に少なくとも1つの設定ミスが存在
- \*\*65%\*\*の環境に高深刻度の設定ミスが存在
- \*\*89%\*\*の組織がKubernetes関連のセキュリティインシデントを経験

本記事では、Kubernetes本番環境で **必ず実装すべき10のセキュリティ設定** を、実際のYAMLマニフェスト例とともに解説します。

### 対象読者

- Kubernetesを本番環境で運用している方
- セキュアなKubernetes環境を構築したい方
- DevSecOpsを推進したい方
- Kubernetesのセキュリティ監査を担当している方

### この記事で学べること

- Pod Security Standardsの実装方法
- RBACによる最小権限の実現
- Network Policyによるネットワーク分離
- Secretsの安全な管理方法
- 実際に使える実践的なYAMLマニフェスト
- セキュリティ設定の検証方法

## 目次

1. [Pod Security Standards (PSS)の実装](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#1-pod-security-standards-pss%E3%81%AE%E5%AE%9F%E8%A3%85)
2. [RBACによる最小権限アクセス制御](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#2-rbac%E3%81%AB%E3%82%88%E3%82%8B%E6%9C%80%E5%B0%8F%E6%A8%A9%E9%99%90%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E5%88%B6%E5%BE%A1)
3. [Network Policyによるネットワーク分離](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#3-network-policy%E3%81%AB%E3%82%88%E3%82%8B%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E5%88%86%E9%9B%A2)
4. [Secretsの暗号化と安全な管理](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#4-secrets%E3%81%AE%E6%9A%97%E5%8F%B7%E5%8C%96%E3%81%A8%E5%AE%89%E5%85%A8%E3%81%AA%E7%AE%A1%E7%90%86)
5. [イメージの脆弱性スキャン](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#5-%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E8%84%86%E5%BC%B1%E6%80%A7%E3%82%B9%E3%82%AD%E3%83%A3%E3%83%B3)
6. [Resource Limits と Quotas](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#6-resource-limits-%E3%81%A8-quotas)
7. [Audit Loggingの有効化](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#7-audit-logging%E3%81%AE%E6%9C%89%E5%8A%B9%E5%8C%96)
8. [Admission Controllerの活用](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#8-admission-controller%E3%81%AE%E6%B4%BB%E7%94%A8)
9. [Security Contextの適切な設定](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#9-security-context%E3%81%AE%E9%81%A9%E5%88%87%E3%81%AA%E8%A8%AD%E5%AE%9A)
10. [ランタイムセキュリティ監視](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#10-%E3%83%A9%E3%83%B3%E3%82%BF%E3%82%A4%E3%83%A0%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3%E7%9B%A3%E8%A6%96)

---

## 1\. Pod Security Standards (PSS)の実装

### なぜ必要か？

Pod Security Standards (PSS)は、Kubernetesクラスタ内のPodに対してセキュリティポリシーを適用するための標準的なフレームワークです。Kubernetes v1.25以降、従来のPodSecurityPolicyは廃止され、PSSが推奨されています。

### 3つのセキュリティレベル

```text
┌────────────────────────────────────────────────────┐
│  Privileged (特権)                                  │
│  • 最も緩い設定                                     │
│  • すべての権限を許可                               │
│  • システムコンポーネント用                          │
└────────────────────────────────────────────────────┘
            ↓ より厳格に
┌────────────────────────────────────────────────────┐
│  Baseline (ベースライン)                            │
│  • 最小限の制約                                     │
│  • 一般的な攻撃ベクトルをブロック                    │
│  • ほとんどのアプリケーションで使用可能              │
└────────────────────────────────────────────────────┘
            ↓ より厳格に
┌────────────────────────────────────────────────────┐
│  Restricted (制限付き)                              │
│  • 最も厳格な設定                                   │
│  • 現在のPod強化ベストプラクティスに準拠             │
│  • 本番環境で推奨                                   │
└────────────────────────────────────────────────────┘
```

### 実装方法

#### Namespace レベルでの適用

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # enforce: ポリシー違反を拒否（本番環境推奨）
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest

    # audit: 違反を監査ログに記録
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest

    # warn: 違反時に警告メッセージを表示
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

**適用:**

```bash
kubectl apply -f namespace.yaml
```

#### Restricted レベルに準拠した Deployment

```yaml
# secure-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      # 1. サービスアカウントの自動マウントを無効化
      automountServiceAccountToken: false

      # 2. セキュリティコンテキスト（Pod レベル）
      securityContext:
        # 非rootユーザーとして実行
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 2000
        # seccompプロファイル（システムコール制限）
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: app
        image: myapp:1.0.0

        # 3. セキュリティコンテキスト（Container レベル）
        securityContext:
          # 特権コンテナを禁止
          privileged: false
          # 権限昇格を禁止
          allowPrivilegeEscalation: false
          # 読み取り専用ルートファイルシステム
          readOnlyRootFilesystem: true
          # Capabilitiesをすべて削除
          capabilities:
            drop:
              - ALL

        # 4. リソース制限（必須）
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi

        # 5. 一時ディレクトリ用のボリューム（readOnlyRootFilesystem使用時）
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache

      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
```

### 検証方法

```bash
# Namespace の PSS 設定を確認
kubectl get namespace production -o yaml | grep pod-security

# ポリシー違反のテスト（拒否されることを確認）
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: privileged-pod
  namespace: production
spec:
  containers:
  - name: test
    image: nginx
    securityContext:
      privileged: true  # ← Restricted レベルでは拒否される
EOF

# 期待される出力:
# Error from server (Forbidden): pods "privileged-pod" is forbidden:
# violates PodSecurity "restricted:latest": privileged
```

### ベストプラクティス

✅ **本番環境**: `restricted` レベルを使用  
✅ **開発環境**: `baseline` レベルから始めて段階的に `restricted` に移行  
✅ **システムコンポーネント**: 専用のNamespaceで `privileged` を使用（kube-system等）  
✅ **段階的移行**: まず `audit` と `warn` モードで影響を確認してから `enforce` を有効化

---

## 2\. RBACによる最小権限アクセス制御

### なぜ必要か？

RBAC (Role-Based Access Control) は、Kubernetesクラスタ内のリソースへのアクセスを制御する仕組みです。最小権限の原則に基づき、必要最小限の権限のみを付与することで、セキュリティリスクを大幅に削減できます。

### RBAC の構成要素

```text
┌─────────────────────────────────────────────────────┐
│  Subject (主体)                                      │
│  • User                                              │
│  • Group                                             │
│  • ServiceAccount ← Podが使用                        │
└─────────────────────────────────────────────────────┘
            ↓ (Binding)
┌─────────────────────────────────────────────────────┐
│  Role / ClusterRole (権限の定義)                     │
│  • Role: Namespace内のリソースへの権限               │
│  • ClusterRole: クラスタ全体のリソースへの権限        │
└─────────────────────────────────────────────────────┘
```

### 危険な設定例（絶対に避けるべき）

```yaml
# ❌ 危険: すべての権限を付与
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: dangerous-binding
subjects:
- kind: User
  name: developer
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin  # ← すべての権限！
  apiGroup: rbac.authorization.k8s.io
```

**問題点:**

- クラスタ内のすべてのリソースに無制限にアクセス可能
- Secretsを含むすべてのデータを閲覧・変更可能
- ノードへのアクセスも可能
- 誤操作や侵害時の影響範囲が最大

### 安全な設定例（最小権限）

#### アプリケーション用 ServiceAccount

```yaml
# serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: production
# 自動でトークンをマウントしない（必要な場合のみ明示的に指定）
automountServiceAccountToken: false

---
# role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: myapp-role
  namespace: production
rules:
# 特定のConfigMapの読み取りのみ
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["myapp-config"]  # ← 特定のリソース名に限定
  verbs: ["get", "list"]

# 特定のSecretの読み取りのみ
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["myapp-secret"]
  verbs: ["get"]

# 自分自身のPodの情報取得（メトリクス用など）
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]

---
# rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: myapp-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: myapp-sa
  namespace: production
roleRef:
  kind: Role
  name: myapp-role
  apiGroup: rbac.authorization.k8s.io
```

#### Deployment での ServiceAccount 使用

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: myapp-sa  # ← 専用のServiceAccountを使用
      automountServiceAccountToken: true  # 必要な場合のみtrue
      containers:
      - name: app
        image: myapp:1.0.0
```

#### 開発者用の Role（Namespace スコープ）

```yaml
# developer-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
  namespace: development
rules:
# Podの作成・削除・確認
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch", "create", "delete"]

# Deploymentの管理
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

# Serviceの管理
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

# ConfigMapの管理
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

# ❌ Secretsへのアクセスは付与しない
# ❌ Nodesへのアクセスは付与しない
# ❌ Namespace作成権限は付与しない

---
# developer-rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: development
subjects:
- kind: User
  name: alice@example.com
  apiGroup: rbac.authorization.k8s.io
- kind: User
  name: bob@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

### 検証方法

```bash
# 現在のユーザーの権限を確認
kubectl auth can-i get pods
kubectl auth can-i delete deployments
kubectl auth can-i get secrets

# 特定のServiceAccountの権限を確認
kubectl auth can-i get secrets --as=system:serviceaccount:production:myapp-sa

# すべての権限を一覧表示
kubectl auth can-i --list

# 特定のNamespaceでの権限を確認
kubectl auth can-i --list --namespace=production
```

### RBAC監査スクリプト

```bash
#!/bin/bash
# rbac-audit.sh - 危険な権限設定を検出

echo "=== RBAC Security Audit ==="

# 1. cluster-admin権限を持つユーザー/SAを検出
echo "📋 ClusterRoleBindings with cluster-admin:"
kubectl get clusterrolebindings -o json | \
  jq -r '.items[] | select(.roleRef.name=="cluster-admin") |
  "\(.metadata.name): \(.subjects[].kind) \(.subjects[].name)"'

# 2. すべてのNamespaceに対するアクセス権を検出
echo -e "\n📋 ClusterRoles with wildcard (*) resources:"
kubectl get clusterroles -o json | \
  jq -r '.items[] | select(.rules[].resources[]? == "*") | .metadata.name'

# 3. Secretsへのアクセス権を持つすべてのRoleを検出
echo -e "\n📋 Roles with secrets access:"
kubectl get roles --all-namespaces -o json | \
  jq -r '.items[] | select(.rules[].resources[]? == "secrets") |
  "\(.metadata.namespace)/\(.metadata.name)"'

# 4. system:masters グループのメンバーを確認（最も危険）
echo -e "\n⚠️  system:masters group members (CRITICAL):"
kubectl get clusterrolebindings -o json | \
  jq -r '.items[] | select(.subjects[]?.name=="system:masters") |
  "\(.metadata.name): \(.subjects[])"'
```

### ベストプラクティス

✅ **最小権限の原則**: 必要最小限の権限のみ付与  
✅ **Namespace スコープ**: 可能な限り `Role` と `RoleBinding` を使用（ClusterRoleより安全）  
✅ **リソース名の指定**: `resourceNames` で特定のリソースに限定  
✅ **system:masters グループの禁止**: 絶対にユーザーを追加しない  
✅ **定期的な監査**: 不要な権限を定期的に見直し  
✅ **ServiceAccount の分離**: アプリケーションごとに専用のServiceAccountを作成

---

## 3\. Network Policyによるネットワーク分離

### なぜ必要か？

デフォルトのKubernetesでは、 **すべてのPodが相互に通信可能** です。これは攻撃者が侵入した場合、横展開（Lateral Movement）を容易にします。Network Policyを使用することで、Pod間の通信を制限し、ゼロトラストネットワークを実現できます。

### デフォルトの危険な状態

```text
┌──────────────────────────────────────────────────┐
│  Default (Network Policy なし)                   │
├──────────────────────────────────────────────────┤
│  Frontend Pod ←→ Backend Pod                     │
│       ↕              ↕                           │
│  Database Pod ←→ Cache Pod                       │
│       ↕              ↕                           │
│  Admin Pod   ←→ Monitoring Pod                   │
│                                                  │
│  すべてのPodが相互に通信可能                      │
│  ← 攻撃者が1つのPodに侵入すると...               │
│     すべてのPodにアクセス可能！                   │
└──────────────────────────────────────────────────┘
```

### Network Policy実装後の安全な状態

```text
┌──────────────────────────────────────────────────┐
│  With Network Policy                             │
├──────────────────────────────────────────────────┤
│  Frontend Pod → Backend Pod (許可)               │
│                    ↓                             │
│                Database Pod (許可)               │
│                                                  │
│  Frontend Pod ╳ Database Pod (拒否)              │
│  Admin Pod ╳ Backend Pod (拒否)                  │
│                                                  │
│  必要な通信のみ許可                               │
│  ← 攻撃者がFrontendに侵入しても、                │
│     Databaseへの直接アクセスは不可               │
└──────────────────────────────────────────────────┘
```

### 基本戦略: デフォルト拒否

```yaml
# deny-all-network-policy.yaml
# すべての Ingress/Egress を拒否（ホワイトリスト方式）
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  podSelector: {}  # すべてのPodに適用
  policyTypes:
  - Ingress
  - Egress
  # rulesが空 = すべて拒否
```

**適用:**

```bash
kubectl apply -f deny-all-network-policy.yaml
```

### 実践例: 3-Tier アプリケーション

#### アーキテクチャ

```text
[Internet]
   ↓
[Ingress Controller]
   ↓
[Frontend Pods] (app=frontend)
   ↓
[Backend Pods] (app=backend)
   ↓
[Database Pods] (app=database)
```

#### Frontend Pod の Network Policy

```yaml
# frontend-network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  - Egress

  # Ingress: Ingress Controllerからのトラフィックのみ許可
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080

  # Egress: Backendへの通信のみ許可
  egress:
  # Backend APIへのアクセス
  - to:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 3000

  # DNS解決のため（必須）
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

#### Backend Pod の Network Policy

```yaml
# backend-network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress

  # Ingress: Frontendからのトラフィックのみ許可
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 3000

  # Egress: Databaseと外部APIへの通信を許可
  egress:
  # Databaseへのアクセス
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432

  # 外部API呼び出し（特定のCIDRに制限）
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 10.0.0.0/8    # 内部ネットワークを除外
        - 172.16.0.0/12
        - 192.168.0.0/16
    ports:
    - protocol: TCP
      port: 443

  # DNS解決
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

#### Database Pod の Network Policy

```yaml
# database-network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
  - Ingress
  - Egress

  # Ingress: Backendからのトラフィックのみ許可
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 5432

  # Egress: 外部への通信を完全に禁止（DNSのみ許可）
  egress:
  # DNS解決のみ
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

### Namespace間の分離

```yaml
# namespace-isolation.yaml
# 異なるNamespace間の通信を制限
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-from-other-namespaces
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  # 同じNamespace内からのトラフィックのみ許可
  - from:
    - podSelector: {}
```

### 検証方法

```bash
# Network Policyの一覧を確認
kubectl get networkpolicies -n production

# 特定のNetwork Policyの詳細を確認
kubectl describe networkpolicy frontend-policy -n production

# 通信テストPodを起動
kubectl run test-pod --image=nicolaka/netshoot -n production -- sleep 3600

# Frontend → Backend の通信テスト（成功するはず）
kubectl exec -it test-pod -n production -- curl http://backend-service:3000

# Frontend → Database の直接通信テスト（失敗するはず）
kubectl exec -it test-pod -n production -- curl http://database-service:5432
# 期待される結果: タイムアウト（通信がブロックされる）
```

### Network Policy可視化ツール

```bash
# kubectl-netshoot プラグインのインストール
kubectl krew install np-viewer

# Network Policyの可視化
kubectl np-viewer -n production

# または、手動で確認
kubectl get networkpolicies -n production -o yaml
```

### ベストプラクティス

✅ **デフォルト拒否**: すべてのNamespaceで `deny-all` ポリシーを適用  
✅ **最小権限通信**: 必要な通信経路のみを明示的に許可  
✅ **DNS許可を忘れない**: ほぼすべてのPodでDNS解決が必要  
✅ **Namespaceラベルの活用**: Namespace間通信の制御に使用  
✅ **定期的なテスト**: Network Policyが意図通りに動作しているか確認  
✅ **ドキュメント化**: 各ポリシーの目的と通信フローを文書化

### 注意点

⚠️ **CNI プラグイン依存**: Network PolicyはCNIプラグイン（Calico、Cilium、Weave Net等）が必要  
⚠️ **AWS EKS**: VPC CNIはNetwork Policyをサポートしていない（Calicoの追加インストールが必要）  
⚠️ **GKE**: Network Policyアドオンを有効化する必要あり  
⚠️ **パフォーマンス**: 大量のポリシーはパフォーマンスに影響する可能性

---

## 4\. Secretsの暗号化と安全な管理

### なぜ必要か？

Kubernetesの **Secretsはデフォルトでetcdに平文で保存** されます。これは、etcdへのアクセス権を持つ攻撃者が、すべてのパスワードやAPIキーを取得できることを意味します。

### 危険なデフォルト設定

```bash
# Secretを作成
kubectl create secret generic db-password --from-literal=password=SuperSecret123

# etcdから直接読み取ると...（etcdへのアクセス権がある場合）
ETCDCTL_API=3 etcdctl get /registry/secrets/default/db-password

# 出力: 平文でパスワードが表示される！
# password: SuperSecret123
```

### 必須設定 1: etcd の暗号化

#### 暗号化設定ファイルの作成

```yaml
# encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    - configmaps  # ConfigMapsも暗号化推奨
    providers:
    # 1. aescbc: 暗号化（推奨）
    - aescbc:
        keys:
        - name: key1
          secret: <BASE64_ENCODED_32_BYTE_KEY>
    # 2. identity: 平文（既存データ読み取り用、削除予定）
    - identity: {}
```

#### 暗号化キーの生成

```bash
# 32バイトのランダムキーを生成
head -c 32 /dev/urandom | base64

# 出力例: K7dFZq8XQ9n+R5tYuVwP2mN8hL1jG4kE3aS6cB7xD9w=
```

#### kube-apiserverの設定

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml（マネージドサービスでは自動設定）
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - name: kube-apiserver
    command:
    - kube-apiserver
    - --encryption-provider-config=/etc/kubernetes/encryption-config.yaml
    volumeMounts:
    - name: encryption-config
      mountPath: /etc/kubernetes/encryption-config.yaml
      readOnly: true
  volumes:
  - name: encryption-config
    hostPath:
      path: /etc/kubernetes/encryption-config.yaml
      type: File
```

#### 既存のSecretsを再暗号化

```bash
# すべてのSecretsを読み取り→書き込み（暗号化される）
kubectl get secrets --all-namespaces -o json | \
  kubectl replace -f -
```

### 必須設定 2: 外部Secrets管理（推奨）

#### AWS Secrets Manager との統合

```yaml
# external-secrets-operator を使用
# https://external-secrets.io/

# SecretStore の定義
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: production
spec:
  provider:
    aws:
      service: SecretsManager
      region: ap-northeast-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa

---
# ExternalSecret の定義
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: production
spec:
  refreshInterval: 1h  # 1時間ごとに同期
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials  # Kubernetes Secret名
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: production/database  # AWS Secrets Manager のキー
      property: username
  - secretKey: password
    remoteRef:
      key: production/database
      property: password
```

#### Deployment での使用

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: production
spec:
  template:
    spec:
      containers:
      - name: app
        image: backend:1.0.0
        env:
        # 環境変数として使用（推奨）
        - name: DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password

        # または、ファイルとしてマウント
        volumeMounts:
        - name: db-credentials
          mountPath: /etc/secrets
          readOnly: true

      volumes:
      - name: db-credentials
        secret:
          secretName: db-credentials
          defaultMode: 0400  # 所有者のみ読み取り可能
```

### 必須設定 3: Secretsローテーション

```yaml
# secrets-rotation-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: secrets-rotation
  namespace: production
spec:
  # 毎月1日の午前2時に実行
  schedule: "0 2 1 * *"
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: secrets-rotator
          containers:
          - name: rotate
            image: bitnami/kubectl:latest
            command:
            - /bin/sh
            - -c
            - |
              # AWS Secrets Managerでパスワードをローテーション
              aws secretsmanager rotate-secret \
                --secret-id production/database \
                --rotation-lambda-arn arn:aws:lambda:...

              # Kubernetes Secretを更新（External Secrets Operatorが自動同期）
              kubectl annotate externalsecret db-credentials \
                force-sync=$(date +%s) \
                -n production --overwrite
          restartPolicy: OnFailure
```

### RBAC: Secretsアクセスの制限

```yaml
# secrets-reader-role.yaml
# ⚠️ 注意: list や watch もSecrets の内容を読み取れる
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secrets-reader
  namespace: production
rules:
# ✅ 特定のSecretのみ読み取り可能
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["app-specific-secret"]  # 特定のSecretに限定
  verbs: ["get"]

# ❌ 危険: すべてのSecretsを列挙可能
# - apiGroups: [""]
#   resources: ["secrets"]
#   verbs: ["list", "watch"]  # これらも内容を読み取れる！
```

### Secretsのベストプラクティス

#### ❌ 避けるべきパターン

```yaml
# 1. ❌ Secretを環境変数として公開（ログに残る可能性）
env:
- name: API_KEY
  value: "sk-1234567890abcdef"  # 平文で記述

# 2. ❌ ConfigMapに機密情報を保存
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database-password: "SuperSecret123"  # ❌ ConfigMapは暗号化されない
```

#### ✅ 推奨パターン

```yaml
# 1. ✅ Secretから環境変数に注入
env:
- name: API_KEY
  valueFrom:
    secretKeyRef:
      name: api-credentials
      key: api-key

# 2. ✅ Secretをファイルとしてマウント（より安全）
volumeMounts:
- name: api-credentials
  mountPath: /etc/secrets
  readOnly: true

volumes:
- name: api-credentials
  secret:
    secretName: api-credentials
    defaultMode: 0400  # 読み取り専用

# アプリケーション内で読み取り
# const apiKey = fs.readFileSync('/etc/secrets/api-key', 'utf8');
```

### 検証方法

```bash
# Secretが暗号化されているか確認（etcdへのアクセスが必要）
ETCDCTL_API=3 etcdctl get /registry/secrets/production/db-credentials

# 出力が "k8s:enc:aescbc:v1:key1:" で始まっていれば暗号化されている
# 平文が見えたら暗号化されていない！

# Secretsへのアクセス権を監査
kubectl auth can-i list secrets --all-namespaces

# 特定のユーザーのSecretsアクセス権を確認
kubectl auth can-i get secrets --as=system:serviceaccount:production:myapp-sa
```

### Secrets監査スクリプト

```bash
#!/bin/bash
# secrets-audit.sh

echo "=== Secrets Security Audit ==="

# 1. Secretsへのアクセス権を持つすべてのRoleを検出
echo "📋 Roles with secrets access:"
kubectl get roles,clusterroles --all-namespaces -o json | \
  jq -r '.items[] | select(.rules[]?.resources[]? == "secrets") |
  "\(.metadata.namespace // "cluster")/\(.metadata.name): \(.rules[] | select(.resources[]? == "secrets") | .verbs)"'

# 2. Secretsを環境変数として使用しているPodを検出（警告）
echo -e "\n⚠️  Pods using Secrets as environment variables:"
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] | select(.spec.containers[].env[]?.valueFrom.secretKeyRef) |
  "\(.metadata.namespace)/\(.metadata.name)"'

# 3. defaultモード以外（0644以外）のSecret volumeを確認
echo -e "\n✅ Secrets with restricted file permissions:"
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] | select(.spec.volumes[]?.secret.defaultMode == 256) |
  "\(.metadata.namespace)/\(.metadata.name)"'
```

### ベストプラクティス

✅ **etcd暗号化**: 必ず有効化（マネージドサービスでは確認）  
✅ **外部Secrets管理**: AWS Secrets Manager、Vault等を使用  
✅ **定期的なローテーション**: 最低90日ごとにローテーション  
✅ **ファイルマウント**: 環境変数より安全  
✅ **アクセス制限**: RBACで最小権限に制限  
✅ **監査ログ**: Secretsへのアクセスを記録  
✅ **コードにハードコードしない**: 絶対に避ける

---

## 5\. イメージの脆弱性スキャン

### なぜ必要か？

コンテナイメージには既知の脆弱性（CVE）が含まれていることが多く、2025年の調査では、 **平均的なコンテナイメージに80個以上のCVEが含まれている** というデータがあります。

### スキャンツールの選択

| ツール | 特徴 | コスト |
| --- | --- | --- |
| **Trivy** | オープンソース、高速、包括的 | 無料 |
| **Snyk** | 開発者フレンドリー、修正提案 | 有料 |
| **Aqua Security** | エンタープライズ向け、統合セキュリティ | 有料 |
| **AWS ECR Scan** | AWS統合、基本スキャン | 無料/有料 |
| **GCR Vulnerability Scanning** | GCP統合 | 無料 |
| **Sysdig** | ランタイム保護統合 | 有料 |

### Trivyによるローカルスキャン

```bash
# Trivyのインストール
brew install aquasecurity/trivy/trivy

# イメージのスキャン
trivy image nginx:latest

# 出力例:
# nginx:latest (debian 11.6)
# ===========================
# Total: 87 (UNKNOWN: 0, LOW: 52, MEDIUM: 23, HIGH: 10, CRITICAL: 2)
#
# ┌────────────────┬──────────────┬──────────┬─────────────────┐
# │    Library     │ Vulnerability│ Severity │ Installed Ver.  │
# ├────────────────┼──────────────┼──────────┼─────────────────┤
# │ openssl        │ CVE-2024-1234│ CRITICAL │ 1.1.1n-0+deb11u3│
# │ libssl1.1      │ CVE-2024-5678│ HIGH     │ 1.1.1n-0+deb11u3│
# └────────────────┴──────────────┴──────────┴─────────────────┘

# CRITICAL/HIGHのみ表示
trivy image --severity CRITICAL,HIGH nginx:latest

# JSON形式で出力
trivy image -f json -o results.json nginx:latest

# 特定のCVEを無視（False Positive）
trivy image --ignorefile .trivyignore nginx:latest
```

### .trivyignore ファイル

```text
# .trivyignore
# False Positiveや対応不可能な脆弱性を無視

# 例: 修正版がリリースされていないCVE
CVE-2024-12345

# 例: 運用上リスクが低いと判断したCVE
CVE-2024-56789

# コメントで理由を記載
# CVE-2024-11111: ベースイメージの更新待ち（vendor対応中）
CVE-2024-11111
```

### CI/CDパイプラインへの統合

#### GitHub Actions

```yaml
# .github/workflows/scan.yaml
name: Container Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Dockerイメージのビルド
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      # Trivyスキャン
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      # GitHub Security タブに結果をアップロード
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

      # CRITICALが見つかったらビルド失敗
      - name: Check for critical vulnerabilities
        run: |
          trivy image --exit-code 1 --severity CRITICAL myapp:${{ github.sha }}
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - scan
  - deploy

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

trivy-scan:
  stage: scan
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy image --exit-code 1 --severity CRITICAL,HIGH $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  allow_failure: false  # CRITICALがあればパイプライン失敗

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/myapp app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
```

### Admission Controllerによるスキャン強制

```yaml
# trivy-admission-controller.yaml
# クラスタにデプロイされる前にスキャン
apiVersion: v1
kind: ConfigMap
metadata:
  name: trivy-config
  namespace: trivy-system
data:
  config.yaml: |
    # CRITICALまたはHIGHの脆弱性があるイメージを拒否
    vulnerabilities:
      enabled: true
      severity: CRITICAL,HIGH

    # ポリシー違反時のアクション
    policy:
      action: reject  # reject または warn

    # 除外設定
    exclude:
      namespaces:
        - kube-system
        - trivy-system

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trivy-admission
  namespace: trivy-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: trivy-admission
  template:
    metadata:
      labels:
        app: trivy-admission
    spec:
      containers:
      - name: trivy
        image: aquasec/trivy-admission:latest
        volumeMounts:
        - name: config
          mountPath: /etc/trivy
      volumes:
      - name: config
        configMap:
          name: trivy-config
```

### レジストリ統合スキャン

#### AWS ECR

```bash
# ECRでイメージスキャンを有効化
aws ecr put-image-scanning-configuration \
  --repository-name myapp \
  --image-scanning-configuration scanOnPush=true

# スキャン結果の確認
aws ecr describe-image-scan-findings \
  --repository-name myapp \
  --image-id imageTag=latest

# CRITICALの数を取得
aws ecr describe-image-scan-findings \
  --repository-name myapp \
  --image-id imageTag=latest \
  --query 'imageScanFindings.findingSeverityCounts.CRITICAL'
```

#### GCR (Google Container Registry)

```bash
# 脆弱性スキャンの有効化（デフォルトで有効）
gcloud container images describe gcr.io/myproject/myapp:latest \
  --show-package-vulnerability

# 特定の深刻度でフィルタ
gcloud container images list-tags gcr.io/myproject/myapp \
  --filter="tags:latest" \
  --format=json | \
  jq '.[0].vulnerabilities | map(select(.severity == "CRITICAL"))'
```

### セキュアなベースイメージの選択

```dockerfile
# ❌ 避けるべき: 古いベースイメージ
FROM ubuntu:18.04  # サポート終了、多数の脆弱性

# ❌ 避けるべき: latestタグ
FROM node:latest  # バージョン固定されていない、再現性なし

# ✅ 推奨: 最新の安定版を明示
FROM node:20.11-alpine3.19

# ✅ さらに推奨: Distrolessイメージ
FROM gcr.io/distroless/nodejs20-debian12
# メリット: 最小限のパッケージ、攻撃対象領域が小さい

# ✅ または: Chainguard Images（セキュリティ重視）
FROM cgr.dev/chainguard/node:latest
```

### Multi-stage Buildでイメージを最小化

```dockerfile
# ビルドステージ
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 実行ステージ（最小限）
FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
# ビルド成果物のみコピー
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
# distrolessはシェルがないので、直接Node.jsを実行
CMD ["dist/index.js"]

# 結果: イメージサイズ 90MB → 50MB、脆弱性 87個 → 3個
```

### 脆弱性対応フロー

```text
1. スキャン実行
   ↓
2. 脆弱性発見
   ↓
3. 深刻度評価 (CVSS Score)
   ├─ CRITICAL (9.0-10.0) → 即座に対応
   ├─ HIGH (7.0-8.9)      → 24時間以内
   ├─ MEDIUM (4.0-6.9)    → 1週間以内
   └─ LOW (0.1-3.9)       → 計画的に対応
   ↓
4. 修正方法の検討
   ├─ パッケージ更新
   ├─ ベースイメージ変更
   ├─ パッチ適用
   └─ 回避策（一時的）
   ↓
5. 再スキャンで確認
   ↓
6. デプロイ
```

### ベストプラクティス

✅ **CI/CDに統合**: すべてのビルドで自動スキャン  
✅ **ゲートとして使用**: CRITICAL脆弱性があればデプロイ拒否  
✅ **定期的な再スキャン**: 既存のイメージも定期的にスキャン  
✅ **ベースイメージの最新化**: 月次で更新  
✅ **Distroless使用**: 攻撃対象領域を最小化  
✅ **SBOM生成**: ソフトウェア部品表を管理  
✅ **脆弱性データベース更新**: Trivyのデータベースを最新に保つ

---

**(続く: 残りの5つのセキュリティ設定は次のセクションで...)**

---

## 6\. Resource Limits と Quotas

### なぜ必要か？

リソース制限がないと、1つのPodがクラスタ全体のリソースを消費し、他のPodが起動できなくなる可能性があります。また、リソース制限は **DoS攻撃やクリプトマイニング攻撃** の影響を最小化する重要な防御層です。

### Pod レベルの Resource Limits

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-demo
spec:
  containers:
  - name: app
    image: nginx
    resources:
      # requests: スケジューリング時の最低保証
      requests:
        cpu: 100m      # 0.1 CPU core
        memory: 128Mi  # 128 MiB

      # limits: 最大使用量（超過すると制限/終了）
      limits:
        cpu: 500m      # 0.5 CPU core
        memory: 512Mi  # 512 MiB
        # ephemeral-storage: 一時ストレージ制限
        ephemeral-storage: 2Gi
```

**動作:**

- **CPU limits超過**: スロットリング（制限）される
- **Memory limits超過**: OOMKilled（Podが強制終了）
- **Storage limits超過**: Podが Evict（退避）される

### Namespace レベルの ResourceQuota

```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    # Compute リソース
    requests.cpu: "10"        # 合計10 CPU cores
    requests.memory: 20Gi     # 合計20 GiB
    limits.cpu: "20"          # 合計20 CPU cores
    limits.memory: 40Gi       # 合計40 GiB

    # ストレージ
    requests.storage: 100Gi   # PVC合計100 GiB
    persistentvolumeclaims: "10"  # PVC数の上限

    # オブジェクト数
    pods: "50"                # Pod数の上限
    services: "20"            # Service数の上限
    secrets: "50"             # Secret数の上限
    configmaps: "50"          # ConfigMap数の上限
```

### LimitRange（デフォルト値の設定）

```yaml
# limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
  # Pod レベルの制限
  - type: Pod
    max:
      cpu: "4"
      memory: 8Gi
    min:
      cpu: 100m
      memory: 64Mi

  # Container レベルの制限
  - type: Container
    # デフォルト値（未指定時に自動設定）
    default:
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    # 最大/最小値
    max:
      cpu: "2"
      memory: 4Gi
    min:
      cpu: 50m
      memory: 32Mi

  # PVC の制限
  - type: PersistentVolumeClaim
    max:
      storage: 10Gi
    min:
      storage: 1Gi
```

### 実践例: マルチテナント環境

```yaml
# team-a-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
---
# team-a-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "5"
    requests.memory: 10Gi
    limits.cpu: "10"
    limits.memory: 20Gi
    pods: "30"
---
# team-a-limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: team-a-limits
  namespace: team-a
spec:
  limits:
  - type: Container
    default:
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    max:
      cpu: "2"
      memory: 4Gi
```

### 検証方法

```bash
# ResourceQuotaの確認
kubectl get resourcequota -n production
kubectl describe resourcequota production-quota -n production

# 出力例:
# Name:                   production-quota
# Namespace:              production
# Resource                Used   Hard
# --------                ----   ----
# limits.cpu              8      20
# limits.memory           16Gi   40Gi
# pods                    25     50
# requests.cpu            4      10
# requests.memory         8Gi    20Gi

# LimitRangeの確認
kubectl get limitrange -n production
kubectl describe limitrange default-limits -n production

# Podのリソース使用状況
kubectl top pods -n production
kubectl top nodes

# リソース制限なしのPodを検出
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] | select(.spec.containers[].resources.limits == null) |
  "\(.metadata.namespace)/\(.metadata.name)"'
```

### クリプトマイニング攻撃への対策

```yaml
# anti-cryptomining-limits.yaml
# クリプトマイニングを困難にする設定
apiVersion: v1
kind: LimitRange
metadata:
  name: anti-cryptomining
  namespace: production
spec:
  limits:
  - type: Container
    # CPU使用量を制限（マイニングは高CPU使用）
    max:
      cpu: "1"      # 1 core以下に制限
    default:
      cpu: 500m
    # CPU throttling を有効にする
    defaultRequest:
      cpu: 100m
```

### ベストプラクティス

✅ **すべてのPodに制限を設定**: LimitRangeでデフォルト値を設定  
✅ **Namespace単位でQuotaを設定**: マルチテナント環境では必須  
✅ **requestsとlimitsを適切に設定**: requests < limits  
✅ **監視とアラート**: リソース使用率を監視  
✅ **定期的な見直し**: アプリケーションの成長に合わせて調整

---

## 7\. Audit Loggingの有効化

### なぜ必要か？

Audit Logは、Kubernetesクラスタで **誰が、いつ、何をしたか** を記録します。セキュリティインシデント発生時の調査や、コンプライアンス対応に必須です。

### Audit Policyの設定

```yaml
# audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
# 1. Secretsへのアクセスをすべて記録（最重要）
- level: RequestResponse
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  resources:
  - group: ""
    resources: ["secrets"]

# 2. 機密性の高いリソースへのアクセスを記録
- level: RequestResponse
  verbs: ["create", "update", "patch", "delete"]
  resources:
  - group: ""
    resources: ["configmaps", "serviceaccounts"]
  - group: "rbac.authorization.k8s.io"
    resources: ["roles", "rolebindings", "clusterroles", "clusterrolebindings"]

# 3. Podの実行（exec）を記録
- level: RequestResponse
  verbs: ["create"]
  resources:
  - group: ""
    resources: ["pods/exec", "pods/portforward", "pods/proxy"]

# 4. 認証失敗を記録
- level: RequestResponse
  users: ["system:anonymous"]

# 5. 読み取り専用操作はMetadataのみ
- level: Metadata
  verbs: ["get", "list", "watch"]

# 6. システムコンポーネントのノイズを削減
- level: None
  users:
  - system:kube-proxy
  - system:kube-scheduler
  - system:kube-controller-manager

# 7. ヘルスチェックは記録しない
- level: None
  nonResourceURLs:
  - /healthz*
  - /version
  - /swagger*
```

**ログレベル:**

- **None**: 記録しない
- **Metadata**: メタデータのみ（リクエスト/レスポンスの本文は含まない）
- **Request**: リクエスト本文を記録
- **RequestResponse**: リクエストとレスポンスの両方を記録（Secrets等で使用）

### kube-apiserverへの設定

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - name: kube-apiserver
    command:
    - kube-apiserver
    # Audit設定
    - --audit-policy-file=/etc/kubernetes/audit-policy.yaml
    - --audit-log-path=/var/log/kubernetes/audit.log
    - --audit-log-maxage=30      # 30日間保持
    - --audit-log-maxbackup=10   # 最大10ファイル
    - --audit-log-maxsize=100    # 100MB
    volumeMounts:
    - name: audit-policy
      mountPath: /etc/kubernetes/audit-policy.yaml
      readOnly: true
    - name: audit-log
      mountPath: /var/log/kubernetes
  volumes:
  - name: audit-policy
    hostPath:
      path: /etc/kubernetes/audit-policy.yaml
      type: File
  - name: audit-log
    hostPath:
      path: /var/log/kubernetes
      type: DirectoryOrCreate
```

### 外部ログシステムへの転送

#### Fluentd設定

```yaml
# fluentd-audit.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: kube-system
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/kubernetes/audit.log
      pos_file /var/log/fluentd-audit.log.pos
      tag kubernetes.audit
      <parse>
        @type json
        time_key timestamp
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    # Elasticsearch/Splunk/CloudWatch Logsに転送
    <match kubernetes.audit>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      index_name kubernetes-audit
      type_name audit
    </match>
```

### 重要イベントのアラート設定

```yaml
# audit-alert-rules.yaml (Prometheus AlertManager)
groups:
- name: kubernetes-audit
  interval: 1m
  rules:
  # Secretsへの不正アクセス検出
  - alert: UnauthorizedSecretsAccess
    expr: |
      count_over_time(kubernetes_audit_event{
        verb=~"get|list",
        objectRef_resource="secrets",
        user_username!~"system:.*"
      }[5m]) > 10
    annotations:
      summary: "異常なSecretsアクセスを検出"
      description: "ユーザー {{ $labels.user_username }} が5分間に10回以上Secretsにアクセス"

  # Pod execの監視
  - alert: PodExecDetected
    expr: |
      kubernetes_audit_event{
        verb="create",
        objectRef_resource="pods",
        objectRef_subresource="exec"
      }
    annotations:
      summary: "Pod exec実行を検出"
      description: "ユーザー {{ $labels.user_username }} がPod {{ $labels.objectRef_name }} でexecを実行"

  # RBAC変更の監視
  - alert: RBACModification
    expr: |
      kubernetes_audit_event{
        verb=~"create|update|patch|delete",
        objectRef_resource=~"roles|rolebindings|clusterroles|clusterrolebindings"
      }
    annotations:
      summary: "RBAC設定が変更されました"
      description: "{{ $labels.user_username }} が {{ $labels.objectRef_resource }} を変更"
```

### 監査ログの分析

```bash
# 1. Secretsへのアクセスを確認
cat /var/log/kubernetes/audit.log | \
  jq 'select(.objectRef.resource == "secrets")' | \
  jq '{user: .user.username, verb: .verb, secret: .objectRef.name, time: .requestReceivedTimestamp}'

# 2. 認証失敗を確認
cat /var/log/kubernetes/audit.log | \
  jq 'select(.responseStatus.code >= 400)' | \
  jq '{user: .user.username, code: .responseStatus.code, reason: .responseStatus.reason, time: .requestReceivedTimestamp}'

# 3. Pod execの実行履歴
cat /var/log/kubernetes/audit.log | \
  jq 'select(.objectRef.subresource == "exec")' | \
  jq '{user: .user.username, pod: .objectRef.name, namespace: .objectRef.namespace, time: .requestReceivedTimestamp}'

# 4. RBAC変更履歴
cat /var/log/kubernetes/audit.log | \
  jq 'select(.objectRef.resource | test("role"))' | \
  jq '{user: .user.username, verb: .verb, resource: .objectRef.resource, name: .objectRef.name, time: .requestReceivedTimestamp}'

# 5. 外部IPからのアクセス
cat /var/log/kubernetes/audit.log | \
  jq 'select(.sourceIPs[0] | test("^(?!10\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.|192\\.168\\.)"))' | \
  jq '{user: .user.username, sourceIP: .sourceIPs[0], verb: .verb, resource: .objectRef.resource}'
```

### ベストプラクティス

✅ **Secretsアクセスは必ず記録**: RequestResponseレベル  
✅ **外部ログシステムに転送**: クラスタ内保存は危険  
✅ **長期保存**: 最低90日、可能なら1年以上  
✅ **リアルタイムアラート**: 重要イベントは即座に通知  
✅ **定期的な分析**: 異常なパターンを検出  
✅ **SIEM統合**: Splunk、Elastic、CloudWatch Insights等と連携

---

## 8\. Admission Controllerの活用

### なぜ必要か？

Admission Controllerは、Kubernetesクラスタに作成されるリソースを **デプロイ前に検証・変更** できる仕組みです。セキュリティポリシーを強制するための最後の防御線です。

### 主要な Admission Controllers

#### 1\. ValidatingAdmissionWebhook（検証）

リソースを拒否または許可します。

#### 2\. MutatingAdmissionWebhook（変更）

リソースを自動的に変更します。

### Open Policy Agent (OPA) Gatekeeper

OPA Gatekeeperは、Kubernetesで最も広く使われているポリシーエンジンです。

#### インストール

```bash
# Gatekeeperのインストール
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.15/deploy/gatekeeper.yaml

# インストール確認
kubectl get pods -n gatekeeper-system
```

#### ConstraintTemplate（ポリシーの定義）

```yaml
# block-privileged-containers.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sblockprivileged
spec:
  crd:
    spec:
      names:
        kind: K8sBlockPrivileged
  targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package k8sblockprivileged

      violation[{"msg": msg}] {
        # Podの特権モードをチェック
        container := input.review.object.spec.containers[_]
        container.securityContext.privileged == true
        msg := sprintf("Privileged container is not allowed: %v", [container.name])
      }

      violation[{"msg": msg}] {
        # ホストネットワークの使用をチェック
        input.review.object.spec.hostNetwork == true
        msg := "Host network is not allowed"
      }

      violation[{"msg": msg}] {
        # ホストPIDの使用をチェック
        input.review.object.spec.hostPID == true
        msg := "Host PID is not allowed"
      }
```

#### Constraint（ポリシーの適用）

```yaml
# enforce-no-privileged.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sBlockPrivileged
metadata:
  name: block-privileged-containers
spec:
  enforcementAction: deny  # deny または dryrun
  match:
    kinds:
    - apiGroups: [""]
      kinds: ["Pod"]
    namespaces:
    - "production"
    - "staging"
    excludedNamespaces:
    - "kube-system"  # システムPodは除外
```

### 実践的なポリシー集

#### 1\. イメージの検証（承認されたレジストリのみ許可）

```yaml
# allowed-repos-template.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sallowedrepos
spec:
  crd:
    spec:
      names:
        kind: K8sAllowedRepos
      validation:
        openAPIV3Schema:
          properties:
            repos:
              type: array
              items:
                type: string
  targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package k8sallowedrepos

      violation[{"msg": msg}] {
        container := input.review.object.spec.containers[_]
        not startswith(container.image, input.parameters.repos[_])
        msg := sprintf("Container image %v is not from approved registry", [container.image])
      }

---
# allowed-repos-constraint.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRepos
metadata:
  name: allowed-container-repos
spec:
  match:
    kinds:
    - apiGroups: [""]
      kinds: ["Pod"]
  parameters:
    repos:
    - "gcr.io/mycompany/"
    - "mycompany.azurecr.io/"
    - "123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/"
```

#### 2\. latestタグの禁止

```yaml
# block-latest-tag-template.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sblocklatesttag
spec:
  crd:
    spec:
      names:
        kind: K8sBlockLatestTag
  targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package k8sblocklatesttag

      violation[{"msg": msg}] {
        container := input.review.object.spec.containers[_]
        image := container.image
        endswith(image, ":latest")
        msg := sprintf("Container %v uses 'latest' tag which is not allowed", [container.name])
      }

      violation[{"msg": msg}] {
        container := input.review.object.spec.containers[_]
        image := container.image
        not contains(image, ":")
        msg := sprintf("Container %v has no tag (defaults to 'latest') which is not allowed", [container.name])
      }
```

#### 3\. リソース制限の強制

```yaml
# require-resources-template.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequireresources
spec:
  crd:
    spec:
      names:
        kind: K8sRequireResources
  targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package k8srequireresources

      violation[{"msg": msg}] {
        container := input.review.object.spec.containers[_]
        not container.resources.limits.cpu
        msg := sprintf("Container %v must have CPU limit", [container.name])
      }

      violation[{"msg": msg}] {
        container := input.review.object.spec.containers[_]
        not container.resources.limits.memory
        msg := sprintf("Container %v must have memory limit", [container.name])
      }

      violation[{"msg": msg}] {
        container := input.review.object.spec.containers[_]
        not container.resources.requests.cpu
        msg := sprintf("Container %v must have CPU request", [container.name])
      }

      violation[{"msg": msg}] {
        container := input.review.object.spec.containers[_]
        not container.resources.requests.memory
        msg := sprintf("Container %v must have memory request", [container.name])
      }
```

#### 4\. ラベルの強制

```yaml
# require-labels-template.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequirelabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequireLabels
      validation:
        openAPIV3Schema:
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package k8srequirelabels

      violation[{"msg": msg}] {
        required := input.parameters.labels[_]
        not input.review.object.metadata.labels[required]
        msg := sprintf("Required label %v is missing", [required])
      }

---
# require-labels-constraint.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequireLabels
metadata:
  name: require-labels
spec:
  match:
    kinds:
    - apiGroups: ["apps"]
      kinds: ["Deployment", "StatefulSet"]
  parameters:
    labels:
    - "app"
    - "environment"
    - "owner"
    - "cost-center"
```

### 検証方法

```bash
# Gatekeeperの状態確認
kubectl get constrainttemplates
kubectl get constraints

# ポリシー違反のテスト（拒否されることを確認）
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: test-privileged
spec:
  containers:
  - name: nginx
    image: nginx:latest
    securityContext:
      privileged: true
EOF

# 期待される出力:
# Error from server (Forbidden): admission webhook "validation.gatekeeper.sh" denied the request:
# [block-privileged-containers] Privileged container is not allowed: nginx

# Dry-run モードでの確認
kubectl apply -f my-deployment.yaml --dry-run=server

# 監査（既存リソースのポリシー違反チェック）
kubectl get constraints -o json | \
  jq -r '.items[] | select(.status.totalViolations > 0) |
  "\(.metadata.name): \(.status.totalViolations) violations"'
```

### ベストプラクティス

✅ **段階的導入**: 最初は `dryrun` モード、その後 `deny` に変更  
✅ **監査の実施**: 既存リソースの違反を定期的にチェック  
✅ **例外の明確化**: 必要な場合は除外設定を文書化  
✅ **CI/CDでの事前チェック**: デプロイ前にポリシー違反を検出  
✅ **ポリシーのバージョン管理**: Gitでポリシーを管理

---

## 9\. Security Contextの適切な設定

（先述のPod Security Standardsと重複するため、追加のベストプラクティスのみ記載）

### 完全なセキュアなSecurity Context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: highly-secure-pod
spec:
  # Pod レベル
  securityContext:
    runAsNonRoot: true
    runAsUser: 10000
    runAsGroup: 10000
    fsGroup: 10000
    fsGroupChangePolicy: "OnRootMismatch"
    seccompProfile:
      type: RuntimeDefault
    # SELinux (必要に応じて)
    seLinuxOptions:
      level: "s0:c123,c456"

  containers:
  - name: app
    image: myapp:1.0.0
    # Container レベル
    securityContext:
      privileged: false
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 10000
      capabilities:
        drop:
        - ALL
        # 必要最小限のcapabilityのみ追加
        add:
        - NET_BIND_SERVICE  # 例: ポート80/443のバインド
      seccompProfile:
        type: RuntimeDefault

    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache

  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

---

## 10\. ランタイムセキュリティ監視

### なぜ必要か？

静的な設定だけでは防げない攻撃（ゼロデイ脆弱性、設定ミスを悪用した攻撃等）に対して、 **ランタイムでの動作監視** が必要です。

### Falco（オープンソース）

#### インストール

```bash
# Helmでインストール
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  --set falco.grpc.enabled=true \
  --set falcosecurity.sidekick.enabled=true
```

#### カスタムルール

```yaml
# custom-rules.yaml
customRules:
  rules-custom.yaml: |-
    # クリプトマイニング検出
    - rule: Detect Crypto Miners
      desc: Detect cryptocurrency mining activity
      condition: >
        spawned_process and
        (proc.name in (xmrig, minergate, ethminer, ccminer) or
         proc.cmdline contains "stratum+tcp" or
         proc.cmdline contains "pool.minexmr.com")
      output: >
        Cryptocurrency mining detected
        (user=%user.name command=%proc.cmdline container=%container.name)
      priority: CRITICAL

    # Secretsファイルへのアクセス
    - rule: Read Sensitive File
      desc: Detect reads of sensitive files
      condition: >
        open_read and
        sensitive_files and
        not trusted_containers
      output: >
        Sensitive file opened for reading
        (user=%user.name file=%fd.name container=%container.name)
      priority: WARNING

    # Shellの起動（予期しない場合）
    - rule: Unexpected Shell in Container
      desc: Detect unexpected shell spawned in container
      condition: >
        spawned_process and
        container and
        proc.name in (sh, bash, zsh, fish) and
        not user_known_shell_spawn
      output: >
        Shell spawned in container
        (user=%user.name shell=%proc.name container=%container.name)
      priority: WARNING
```

### Sysdig（エンタープライズ）

```yaml
# sysdig-agent-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: sysdig-agent
  namespace: sysdig-agent
spec:
  selector:
    matchLabels:
      app: sysdig-agent
  template:
    metadata:
      labels:
        app: sysdig-agent
    spec:
      hostNetwork: true
      hostPID: true
      tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/master
      containers:
      - name: sysdig-agent
        image: sysdig/agent:latest
        securityContext:
          privileged: true
        env:
        - name: ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: sysdig-agent
              key: access-key
        - name: COLLECTOR
          value: "ingest-us2.app.sysdig.com"
        volumeMounts:
        - name: docker-sock
          mountPath: /host/var/run/docker.sock
        - name: dev
          mountPath: /host/dev
        - name: proc
          mountPath: /host/proc
          readOnly: true
        - name: boot
          mountPath: /host/boot
          readOnly: true
        - name: modules
          mountPath: /host/lib/modules
          readOnly: true
        - name: usr
          mountPath: /host/usr
          readOnly: true
      volumes:
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
      - name: dev
        hostPath:
          path: /dev
      - name: proc
        hostPath:
          path: /proc
      - name: boot
        hostPath:
          path: /boot
      - name: modules
        hostPath:
          path: /lib/modules
      - name: usr
        hostPath:
          path: /usr
```

### ベストプラクティス

✅ **eBPF技術の活用**: 低オーバーヘッドでカーネルレベル監視  
✅ **異常検知**: ベースライン学習と異常検知  
✅ **即座のアラート**: Slack、PagerDuty等に通知  
✅ **フォレンジック**: インシデント調査用のデータ保存  
✅ **自動対応**: 危険なプロセスの自動停止

---

## まとめ

### 10のセキュリティ設定チェックリスト

```text
□ 1. Pod Security Standards を Restricted レベルで実装
□ 2. RBAC で最小権限アクセス制御を実施
□ 3. Network Policy でデフォルト拒否とホワイトリスト化
□ 4. Secrets を etcd 暗号化 + 外部管理
□ 5. イメージ脆弱性スキャンを CI/CD に統合
□ 6. Resource Limits と Quotas を全 Namespace に設定
□ 7. Audit Logging を有効化し外部転送
□ 8. Admission Controller でポリシーを強制
□ 9. Security Context を適切に設定
□ 10. ランタイムセキュリティ監視を導入
```

### セキュリティ成熟度モデル

```text
Level 1: 基本（最低限）
├─ Pod Security Standards (Baseline)
├─ 基本的な RBAC
└─ Resource Limits

Level 2: 中級（推奨）
├─ Pod Security Standards (Restricted)
├─ Network Policy
├─ Secrets 暗号化
├─ イメージスキャン
└─ Audit Logging

Level 3: 上級（ベストプラクティス）
├─ Admission Controller
├─ 外部 Secrets 管理
├─ ランタイムセキュリティ監視
├─ 自動修復
└─ SIEM 統合

Level 4: エキスパート（エンタープライズ）
├─ ゼロトラスト実装
├─ AI による異常検知
├─ 自動インシデント対応
└─ コンプライアンス自動化
```

### 次のステップ

1. **現状評価**: 現在のクラスタで10項目のうちいくつ実装済みか確認
2. **優先順位付け**: リスクの高い項目から実装
3. **段階的導入**: 一度にすべて実装せず、1つずつ確実に
4. **定期的な監査**: 最低月1回はセキュリティ設定を見直し
5. **チームの教育**: セキュリティはツールだけでなく、人の意識が重要

### 参考リンク

- [Kubernetes公式セキュリティドキュメント](https://kubernetes.io/docs/concepts/security/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NSA/CISA Kubernetes Hardening Guide](https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/2716980/nsa-cisa-release-kubernetes-hardening-guidance/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
- [Falco](https://falco.org/)
- [Sysdig](https://sysdig.com/)

---

**この記事が役に立ったら、いいねとストックをお願いします！**

**質問やフィードバックがあれば、コメント欄でお気軽にどうぞ！**

[0](https://qiita.com/keitah/items/?utm_campaign=post_article&utm_medium=twitter&utm_source=twitter_share#comments)

コメント一覧へ移動

X（Twitter）でシェアする

Facebookでシェアする

はてなブックマークに追加する

## Qiita Advent Calendar 開催！

[13](https://qiita.com/keitah/items/c25440de24eea858a24b/likers)

いいねしたユーザー一覧へ移動

14