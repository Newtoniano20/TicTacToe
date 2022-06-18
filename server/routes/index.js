var express = require('express');
var router = express.Router();

class Person {
  constructor(Username, id, match) {
    this.Username = Username;
    this.id = id;
    this.match = match;
  }
}
class Match {
  static lastKey = 0;
  key;
  constructor(P1, P2) {
    this.playing = P1["id"];
    this.not_playing = P2["id"];
    this.P1 = P1;
    this.P2 = P2;
    this.WON = null;
    this.ended = false;
    this.id = ++Match.lastKey;
    this.BOARD = ["", "", "", "", "", "", "", "", ""];
  }
}

var PLAYERS_ONLINE = []
var MATCHES = []
var QUEUE = []
var player_id = 0;
var match_id = 0;

router.post('/update/:match_id/:player_id', (req, res, next)=>{
  change = req.body["change"]
  coords = req.body["coords"]
  match_id = req.params.match_id;
  playing_id = req.params.player_id;
  console.log("MATCH ID:", MATCHES[match_id-1]["playing"], "Player ID", playing_id)
if (MATCHES[match_id-1]["playing"] == playing_id){
  MATCHES[match_id-1]["playing"] = MATCHES[match_id-1]["not_playing"];
  MATCHES[match_id-1]["not_playing"] = playing_id;
  MATCHES[match_id-1]["BOARD"][coords] = change
  BOARD = MATCHES[match_id-1]["BOARD"];
  console.log(BOARD[0], BOARD[1], BOARD[2])
  WIN_POSSIBILITIES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
  for(let POS of WIN_POSSIBILITIES) {
    if (String(BOARD[POS[0]]) === String(BOARD[POS[1]]) & String(BOARD[POS[1]]) === String(BOARD[POS[2]]) & String(BOARD[POS[1]]) != ""){
      MATCHES[match_id-1]["ended"] = true
      MATCHES[match_id-1]["WON"] = String(BOARD[POS[1]])
    }
  }
  res.status(200).send("Done")
}else{
  res.status(101).send("Error: Player is not allowed to move")
}
})

router.get('/game/:match_id', (req, res, next)=>{
  match_id = req.params.match_id;
  res.status(200).send(MATCHES[match_id-1]);
})

router.post('/auth', (req, res)=>{
  let body = req.body;
  let user = body["user"];
  let New_user = new Person(user, player_id, null)
  QUEUE.push(New_user);
  if (QUEUE.length >= 2) {
    P1 = QUEUE.shift()
    P2 = QUEUE.shift()
    NEW_MATCH = new Match(P1, P2)
    MATCHES.push(NEW_MATCH);
    P1["match"] = NEW_MATCH["id"];
    P2["match"] = NEW_MATCH["id"];
    PLAYERS_ONLINE.push(P1);
    PLAYERS_ONLINE.push(P2);
  }
  player_id += 1;
  console.log(MATCHES);
  res.status(200).send(New_user)
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
      if (MATCHES[match_id-1]["P1"]["id"] == user_id){
        VS_PLAYER = MATCHES[match_id-1]["P2"];
      }else{
        VS_PLAYER = MATCHES[match_id-1]["P1"];
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
