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

const createBody = new SharedArray("body", () => {
  const bodies = [];
  for (let i = 0; i < 100; i++) {
    const newBody = {
      title: `Title ${i}`,
      content: `Content ${i}`,
    };
    bodies.push(newBody);
  }
  return bodies;
});

export default () => {
  const randomBody = createBody[Math.floor(Math.random() * createBody.length)];
  http.post("http://localhost:8080/notes", JSON.stringify(randomBody), {
    headers: { "Content-Type": "application/json" },
  });
  sleep(1);
};
