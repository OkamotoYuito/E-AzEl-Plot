# ベースイメージとしてNode.jsのLTSバージョンを使用
FROM node:18-alpine AS base

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のインストールに必要なファイルをコピー
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* /app/
# RUN corepack enable # pnpm を使う場合など

# ビルドステージ
FROM base AS builder
RUN yarn install --frozen-lockfile # または npm install --legacy-peer-deps や pnpm install --frozen-lockfile
COPY . /app/
RUN yarn build # または npm run build や pnpm build

# プロダクションステージ
FROM base AS runner
COPY --from=builder /app/.next /app/.next/
COPY --from=builder /app/public /app/public/
COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/node_modules /app/node_modules/ # 開発時の依存も含む場合。本番用のみにする場合は調整

# Railwayが提供するPORT環境変数を使用し、0.0.0.0でリッスン
ENV PORT 3000
EXPOSE 3000
CMD ["yarn", "start"] # または npm start や pnpm start 