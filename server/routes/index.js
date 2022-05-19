var express = require('express');
var router = express.Router();

var PLAYERS_ONLINE = []
var MATCHES = []
var QUEUE = []
let id = 0;


function NewUser(req, res, next) {
  body = req.body;
  user = body["user"];
  QUEUE.push([user, id]);
  id += 1;
  res.status(200).send(QUEUE)
  next();
}

function StartMatch(req, res, next){
  if (PLAYERS_ONLINE.includes(user)){
    
  }
}

function CheckQueue(req, res, next){
  INGAME = false
  VS_PLAYER = ""
  body = req.body;
  user = body["user"];
  if (PLAYERS_ONLINE.includes(user)){
   INGAME = true
   VS_PLAYER = 
  }
    res.status(200).send({
      "ingame": INGAME,
      "Versus": VS_PLAYER
    })
  next();
}
router.post('/auth', NewUser, (req, res)=>{
  if (QUEUE.length >= 2) {
    P1 = QUEUE.shift()
    P2 = QUEUE.shift()
    MATCHES.push([P1, P2]);
    PLAYERS_ONLINE.push(P1);
    PLAYERS_ONLINE.push(P2);
  }
  console.log(MATCHES);
});

router.get('/queue', CheckQueue, StartMatch)
module.exports = router;
