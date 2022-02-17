#!/usr/bin/env python3
#"shebang"，指定由哪个解释器来执行脚本
#
# Copyright (c) 2019-2021 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

##########################################################################################################
## 调用 python package lgsvl：

from environs import Env
# 与 LG simulator 交互的类和函数是由 python package lgsvl 提供的，因此在 python 程序中首先要调用 lgsvl
import lgsvl

print("Python API Quickstart #1: Connecting to the Simulator")
env = Env()

##########################################################################################################
## 与 simulator 建立连接

# Connects to the simulator instance at the ip defined by LGSVL__SIMULATOR_HOST, default is localhost or 127.0.0.1
# env.str() is equivalent to os.environ.get()
# env.int() is equivalent to int(os.environ.get())

# python 程序需要知道跟哪个 simulator 互动，就需要建立 python 程序和 simulator 的连接。
# 这本质上是在 python 程序中实体化 Simulator 类的一个对象，送入两个参数：simulator 所在的 IP 地址和程序占用的端口
sim = lgsvl.Simulator("localhost", 8181) # 本机，8181 是 simulator 默认使用的端口
# 或者
#sim = lgsvl.Simulator("IP_ADDRESS", 8181)  # 其中 IP_ADDRESS 替换为远程主机的 IP

#sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host), env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))
#sim = lgsvl.Simulator(env.str("localhost", lgsvl.wise.SimulatorSettings.simulator_host), env.int("localhost", lgsvl.wise.SimulatorSettings.simulator_port))

print("Version =", sim.version)
print("Current Time =", sim.current_time)
print("Current Frame =", sim.current_frame)

##########################################################################################################
## 加载仿真环境

# 通过 Simulator 类的 load() 函数实现，例如加载 BorregasAve 环境：
#sim.load("BorregasAve")
# 目前可用的仿真环境如下: 

# 在仿真运行过程中，有时并不是零启动加载环境，而是已经在环境中，需要重置到初始状态，即只保留仿真环境，清空所有加载的车辆和行人，这时可以用 reset() 函数，速度比 load() 更快
# if sim.current_scene == "BorregasAve":   # 判断是否已经在仿真环境中了
#   sim.reset()
# else:
#   sim.load("BorregasAve")

if sim.current_scene == lgsvl.wise.DefaultAssets.map_borregasave:
    sim.reset()
else:
    sim.load(lgsvl.wise.DefaultAssets.map_borregasave)

##########################################################################################################
## 添加本车 (Ego vehicle)，其他车辆 （NPC）和行人

# 向环境中添加本车（只能添加一辆）、其他车辆（可以多辆）、行人（可以多人）都是通过 Simulator 类的 add_agent() 函数实现，例如
# 第一个参数是添加个体的名称，第二个参数是该个体的类型，

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]

ego = sim.add_agent(name = "Lincoln2017MKZ (Apollo 5.0)", agent_type = lgsvl.AgentType.EGO, state = None)
# agent_type：AgentType.EGO - EGO vehicle、AgentType.NPC - NPC vehicle、AgentType.PEDESTRIAN - pedestrian

