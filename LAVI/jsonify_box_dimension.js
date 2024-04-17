const fs = require("fs");

const text = `UL1001: 10 x 10 x 10 inches
UL1002: 12 x 8 x 6 inches
UL1003: 14 x 10 x 8 inches
UL1004: 16 x 12 x 10 inches
UL1005: 18 x 14 x 12 inches
UL1006: 20 x 20 x 20 inches
UL1007: 22 x 22 x 22 inches
UL1008: 24 x 24 x 24 inches
UL1009: 26 x 26 x 26 inches
UL1010: 28 x 28 x 28 inches
UL1011: 21 x 21 x 21 inches
UL1012: 22 x 22 x 22 inches
UL1013: 23 x 23 x 23 inches
UL1014: 24 x 24 x 24 inches
UL1015: 25 x 25 x 25 inches
UL1016: 26 x 26 x 26 inches
UL1017: 27 x 27 x 27 inches
UL1018: 28 x 28 x 28 inches
UL1019: 29 x 29 x 29 inches
UL1020: 30 x 30 x 30 inches
UL1021: 31 x 31 x 31 inches
UL1022: 32 x 32 x 32 inches
UL1023: 33 x 33 x 33 inches
UL1024: 34 x 34 x 34 inches
UL1025: 35 x 35 x 35 inches
UL1026: 36 x 36 x 36 inches
UL1027: 37 x 37 x 37 inches
UL1028: 38 x 38 x 38 inches
UL1029: 39 x 39 x 39 inches
UL1030: 40 x 40 x 40 inches
UL1031: 41 x 41 x 41 inches
UL1032: 42 x 42 x 42 inches
UL1033: 43 x 43 x 43 inches
UL1034: 44 x 44 x 44 inches
UL1035: 45 x 45 x 45 inches
UL1036: 46 x 46 x 46 inches
UL1037: 47 x 47 x 47 inches
UL1038: 48 x 48 x 48 inches
UL1039: 49 x 49 x 49 inches
UL1040: 50 x 50 x 50 inches
UL1041: 51 x 51 x 51 inches
UL1042: 52 x 52 x 52 inches
UL1043: 53 x 53 x 53 inches
UL1044: 54 x 54 x 54 inches
UL1045: 55 x 55 x 55 inches
UL1046: 56 x 56 x 56 inches
UL1047: 57 x 57 x 57 inches
UL1048: 58 x 58 x 58 inches
UL1049: 59 x 59 x 59 inches
UL1050: 60 x 60 x 60 inches`;

const lines = text.split("\n");
const boxes = [];

for (const line of lines) {
  const [id, dimensions] = line.split(": ");
  const [length, width, height] = dimensions
    .split(" x ")
    .map((s) => Number(s.replace(" inches", "")));
  const box = { id, dimensions: { length, width, height, unit: "inches" } };
  boxes.push(box);
}

const json = JSON.stringify(boxes, null, 2);
fs.writeFileSync("data/Fictional_Box_Dimensions.json", json);
