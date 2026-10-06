// Board image coordinates (1448 × 1086). These follow the playable road from
// START around the left loop and across the lower road to FINISH.
window.BOARD_SPACES = [
  [65,994,"start"], [64,866,"cue"], [64,801,"payoff"], [64,711,"cue"],
  [66,641,"plus"], [65,570,"free"], [66,500,"info"], [68,421,"plus"],
  [83,365,"detention"], [122,307,"situation"], [220,318,"plus"],
  [312,374,"payoff"], [374,429,"detention"], [378,499,"situation"],
  [341,550,"free"], [250,703,"payoff"], [251,757,"power"],
  [261,834,"cue"], [330,873,"plus"], [422,891,"payoff"],
  [526,875,"power"], [621,817,"social"], [675,763,"encounter"],
  [810,743,"charades"], [944,741,"encounter"], [1052,741,"social"],
  [1137,760,"trouble"], [1227,771,"plus"], [1269,825,"power"],
  [1318,920,"encounter"], [1372,1007,"social"], [1246,1012,"payoff"],
  [1127,1012,"finish"]
].map(([x,y,type],index)=>({x,y,type,index}));

// The upper and central branches remain reachable in drag mode. They are
// mapped as independent spaces so the facilitator can use the full board.
window.EXTRA_SPACES = [
  [286,94,"free"], [379,83,"plus"], [468,69,"situation"],
  [570,68,"encounter"], [692,72,"free"], [778,103,"payoff"],
  [872,112,"situation"], [979,113,"payoff"], [1075,114,"free"],
  [1156,115,"power"], [1228,173,"free"], [842,165,"payoff"],
  [822,223,"situation"], [781,284,"power"], [743,351,"free"],
  [731,415,"plus"], [731,480,"power"], [706,544,"plus"],
  [742,613,"social"], [789,680,"trouble"], [384,1017,"power"],
  [478,1015,"situation"], [575,1015,"plus"], [675,1005,"social"],
  [756,989,"power"], [775,930,"payoff"], [790,866,"situation"],
  [795,812,"plus"], [212,1010,"temper"]
].map(([x,y,type],index)=>({x,y,type,index:index+window.BOARD_SPACES.length,extra:true}));
