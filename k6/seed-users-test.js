import { sleep } from "k6";
import { SharedArray } from "k6/data";
import http from "k6/http";

export let options = {
  stages: [
    { duration: "30s", target: 400 }, // simulate ramp-up of traffic from 1 to 200 users over 30 seconds.
    { duration: "1m", target: 400 }, // stay at 200 users for 1 minutes
    { duration: "30s", target: 0 }, // ramp-down to 0 users
  ],
  thresholds: {
    http_req_duration: ["p(95)<100"], // 95% of requests must complete below 250ms
  },
};

const getRandomUser = () => {
  const names = [
    "John",
    "Jane",
    "Alice",
    "Bob",
    "Emma",
    "Michael",
    "Eve",
    "David",
    "Sarah",
    "Tom",
  ];
  const randomNameIndex = Math.floor(Math.random() * names.length);
  const name = names[randomNameIndex];
  const domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"];
  const randomEmailIndex = Math.floor(Math.random() * domains.length);
  const username = name.toLowerCase();
  const domain = domains[randomEmailIndex];
  const email = `${username}@${domain}`;
  return { name, email };
};

const createUsersArray = new SharedArray("body", () => {
  const bodies = [];
  for (let i = 0; i < 100; i++) {
    const newBody = getRandomUser();
    bodies.push(newBody);
  }
  return bodies;
});

export default () => {
  const randomUser =
    createUsersArray[Math.floor(Math.random() * createUsersArray.length)];
  http.post("http://localhost:8080/users", JSON.stringify(randomUser), {
    headers: { "Content-Type": "application/json" },
  });
  sleep(1);
};
