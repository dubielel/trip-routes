FROM node:lts-bookworm AS build

WORKDIR /app

COPY package.json .

# --legacy-peer-deps is needed due to an incompatibility between the React 19 and mui-color-input
RUN npm install --legacy-peer-deps

COPY . .

RUN npm run build

FROM nginx:stable-bookworm

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 3000

ENTRYPOINT ["nginx", "-g", "daemon off;"]