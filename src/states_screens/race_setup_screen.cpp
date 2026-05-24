//  SuperTuxKart - a fun racing game with go-kart
//  Copyright (C) 2009-2015 Marianne Gagnon

#include "states_screens/race_setup_screen.hpp"

#include "config/user_config.hpp"
#include "guiengine/widgets/ribbon_widget.hpp"
#include "input/input_manager.hpp"
#include "race/race_manager.hpp"
#include "states_screens/offline_kart_selection.hpp"
#include "states_screens/state_manager.hpp"

const int CONFIG_CODE_NORMAL = 0;

using namespace GUIEngine;

// -----------------------------------------------------------------------------

RaceSetupScreen::RaceSetupScreen() : Screen("race_setup.stkgui")
{
}   // RaceSetupScreen

// -----------------------------------------------------------------------------

void RaceSetupScreen::loadedFromFile()
{
}   // loadedFromFile

// -----------------------------------------------------------------------------

void RaceSetupScreen::init()
{
    Screen::init();
    input_manager->setMasterPlayerOnly(true);

    RaceManager::get()->setMajorMode(RaceManager::MAJOR_MODE_SINGLE);
    RaceManager::get()->setMinorMode(RaceManager::MINOR_MODE_NORMAL_RACE);
    UserConfigParams::m_game_mode = CONFIG_CODE_NORMAL;
    RaceManager::get()->setNumKarts(UserConfigParams::m_default_num_karts);

    UserConfigParams::m_difficulty = RaceManager::DIFFICULTY_MEDIUM;
    RaceManager::get()->setDifficulty(RaceManager::DIFFICULTY_MEDIUM);
}   // init

// -----------------------------------------------------------------------------
void RaceSetupScreen::eventCallback(Widget* widget, const std::string& name,
                                    const int playerID)
{
    if (name == "difficulty")
    {
        assignDifficulty();

        KartSelectionScreen* s = OfflineKartSelectionScreen::getInstance();
        s->setMultiplayer(false);
        s->setFromOverworld(false);
        s->push();
    }
    else if (name == "back")
    {
        StateManager::get()->escapePressed();
    }
}   // eventCallback

// -----------------------------------------------------------------------------
void RaceSetupScreen::assignDifficulty()
{
    UserConfigParams::m_difficulty = RaceManager::DIFFICULTY_MEDIUM;
    RaceManager::get()->setDifficulty(RaceManager::DIFFICULTY_MEDIUM);
}   // assignDifficulty

// -----------------------------------------------------------------------------
