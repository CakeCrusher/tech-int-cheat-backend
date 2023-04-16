// create a new express app
const dotenv = require("dotenv");
dotenv.config();
const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.get("/infer_code", async (req, res) => {
  // get param "command" from request
  
  let command = decodeURIComponent(req.query.command);;
  command = `// ${command}\n console.log("starting")`

  const { data } = await axios.post(
    "https://api.openai.com/v1/engines/code-davinci-002/completions",
    {
      prompt: "<|endoftext|>" + command + "\n--\nLabel:",
      max_tokens: 100,
      temperature: 0,
    },
    {
      headers: {
        Authorization: `Bearer ${process.env.API_KEY}`,
        "Content-Type": "application/json",
      },
    }
  );
  
  const output = data.choices[0].text

  // send back the response as json
  res.json({ output });

})

app.listen(process.env.PORT, () => {
  console.log("Example app listening on port 3000!");
});
