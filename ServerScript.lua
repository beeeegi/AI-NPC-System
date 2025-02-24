local http = game:GetService("http")
local plrs = game:GetService("Players")
local cs = game:GetService("Chat")
local rs = game:GetService("ReplicatedStorage")

local event = rs:WaitForChild("DisplayResponse")

local function getAIResponse(player:Player, message:string)
	local requestData = {
		player_id = tostring(player.UserId), 
		message = message
	}

	local success, response = pcall(function()
		return http:PostAsync("http://IP_ADRESS:PORT/chat", http:JSONEncode(requestData), Enum.HttpContentType.ApplicationJson)
	end)

	if success then
		local responseData = http:JSONDecode(response)
		return responseData.reply
	else
		warn(response)
		return "Communication disrupted... The Organisation is listening!"
	end
end

local function sendChatMsg(text:string)
	event:FireAllClients("<font color='#B22222'>[Okabe]</font> -> " .. text)
end

local function handlePlayerChat(player, message)
	if message ~= "" then
		local npcResponse = getAIResponse(player, message)

		local npc = workspace:FindFirstChild("Okabe")
		if npc and npc:FindFirstChild("Head") then
			cs:Chat(npc.Head, npcResponse, Enum.ChatColor.Blue)
			sendChatMsg(npcResponse)
		end
	end
end

plrs.PlayerAdded:Connect(function(player)
	player.Chatted:Connect(function(message)
		handlePlayerChat(player, message)
	end)
end)
