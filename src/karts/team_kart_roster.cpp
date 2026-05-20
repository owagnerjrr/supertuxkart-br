//
//  SuperTuxKart - a fun racing game with go-kart
//

#include "karts/team_kart_roster.hpp"

TeamKartRoster::TeamKartRoster()
{
    m_front_is_active = true;
}

// ----------------------------------------------------------------------------
TeamKartRoster::TeamKartRoster(const std::string& front_rider_ident,
                               const std::string& rear_rider_ident)
{
    setRiders(front_rider_ident, rear_rider_ident);
}

// ----------------------------------------------------------------------------
void TeamKartRoster::setRiders(const std::string& front_rider_ident,
                               const std::string& rear_rider_ident)
{
    m_front_rider_ident = front_rider_ident;
    m_rear_rider_ident = rear_rider_ident;
    m_front_is_active = true;
}

// ----------------------------------------------------------------------------
void TeamKartRoster::swapRiders()
{
    if (!hasTwoRiders())
        return;

    m_front_is_active = !m_front_is_active;
}

// ----------------------------------------------------------------------------
const std::string& TeamKartRoster::getActiveRiderIdent() const
{
    return m_front_is_active ? m_front_rider_ident : m_rear_rider_ident;
}

// ----------------------------------------------------------------------------
const std::string& TeamKartRoster::getItemRiderIdent() const
{
    return m_front_is_active ? m_rear_rider_ident : m_front_rider_ident;
}

// ----------------------------------------------------------------------------
bool TeamKartRoster::hasTwoRiders() const
{
    return !m_front_rider_ident.empty() && !m_rear_rider_ident.empty();
}

