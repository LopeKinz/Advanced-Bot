import leveling

#register user
leveling.register(user_id)

#add xp
leveling.addxp(user_id,"XP_Number")

#add level
leveling.addlvl(user_id,"LVL_Number")

#get level
level = leveling.getlvl(user_id)

#get XP
xp = leveling.getxp(user_id)

#reset xp
leveling.resetxp(user_id)

#logs
leveling.log_register(user_id)