var express = require('express');
var router = express.Router();

class Person {
  constructor(Username, id, match) {
    this.Username = Username;
    this.id = id;
    this.match = match
  }
}
class Match {
  constructor(P1, P2, id) {
    this.P1 = P1;
    this.P2 = P2;
    this.id = id;
    this.BOARD = ["", "", "", "", "", "", "", "", ""]
  }
}

var PLAYERS_ONLINE = []
var MATCHES = []
var QUEUE = []
let player_id = 0;
let match_id = 0;


function NewUser(req, res, next) {
  let body = req.body;
  let user = body["user"];
  let New_user = new Person(user, player_id, null)
  QUEUE.push(New_user);
  player_id += 1;
  res.status(200).send(New_user)
  next();
}

router.post('/update/:match_id', (req, res, next)=>{
  change = req.body["change"]
  coords = req.body["coords"]
  match_id = req.params.match_id;
  MATCHES[match_id]["BOARD"][coords] = change
  res.status(200).send("Done")
})

router.get('/game/:match_id', (req, res, next)=>{
  match_id = req.params.match_id;
  res.status(200).send(MATCHES[match_id]);
})

router.post('/auth', NewUser, (req, res)=>{
  if (QUEUE.length >= 2) {
    P1 = QUEUE.shift()
    P2 = QUEUE.shift()
    MATCHES.push(new Match(P1, P2, match_id));
    P1["match"] = match_id;
    P2["match"] = match_id;
    match_id += 1;
    PLAYERS_ONLINE.push(P1);
    PLAYERS_ONLINE.push(P2);
  }
  console.log(MATCHES);
});

router.get('/queue/:user_id', (req, res, next) => {
  let INGAME = false
  let match_id = null
  let VS_PLAYER = null
  let user_id = req.params.user_id;
  for (var i = 0; i < PLAYERS_ONLINE.length; i++) {
    if (PLAYERS_ONLINE[i]["id"] == user_id){
      INGAME = true
      match_id = PLAYERS_ONLINE[i]["match"]
      if (MATCHES[match_id]["P1"]["id"] == user_id){
        VS_PLAYER = MATCHES[match_id]["P2"];
      }else{
        VS_PLAYER = MATCHES[match_id]["P1"];
      }
    }
  }
  res.status(200).send({
    "ingame": INGAME,
    "Versus": VS_PLAYER,
    "match_id": match_id
  })
})


module.exports = router;
