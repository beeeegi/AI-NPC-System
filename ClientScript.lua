local rs = game:GetService("ReplicatedStorage")
local tcs = game:GetService("TextChatService")

local event = rs:WaitForChild("DisplayResponse")

event.OnClientEvent:Connect(function(chatMessage)
	tcs.TextChannels.RBXSystem:DisplaySystemMessage(chatMessage)
end)
