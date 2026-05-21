//
//  SuperTuxKart - a fun racing game with go-kart
//

#include "karts/team_kart_roster.hpp"

TeamKartRoster::RiderItemSlot::RiderItemSlot()
{
    m_has_item = false;
}

// ----------------------------------------------------------------------------
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
    clearFrontRiderItem();
    clearRearRiderItem();
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

// ----------------------------------------------------------------------------
TeamKartRoster::RiderItemSlot& TeamKartRoster::getActiveItemSlot()
{
    return m_front_is_active ? m_front_item : m_rear_item;
}

// ----------------------------------------------------------------------------
TeamKartRoster::RiderItemSlot& TeamKartRoster::getReserveItemSlot()
{
    return m_front_is_active ? m_rear_item : m_front_item;
}

// ----------------------------------------------------------------------------
const TeamKartRoster::RiderItemSlot& TeamKartRoster::getActiveItemSlot() const
{
    return m_front_is_active ? m_front_item : m_rear_item;
}

// ----------------------------------------------------------------------------
const TeamKartRoster::RiderItemSlot& TeamKartRoster::getReserveItemSlot() const
{
    return m_front_is_active ? m_rear_item : m_front_item;
}

// ----------------------------------------------------------------------------
void TeamKartRoster::setFrontRiderItem(const std::string& item_ident)
{
    m_front_item.m_item_ident = item_ident;
    m_front_item.m_has_item = !item_ident.empty();
}

// ----------------------------------------------------------------------------
void TeamKartRoster::setRearRiderItem(const std::string& item_ident)
{
    m_rear_item.m_item_ident = item_ident;
    m_rear_item.m_has_item = !item_ident.empty();
}

// ----------------------------------------------------------------------------
void TeamKartRoster::setActiveRiderItem(const std::string& item_ident)
{
    RiderItemSlot& slot = getActiveItemSlot();
    slot.m_item_ident = item_ident;
    slot.m_has_item = !item_ident.empty();
}

// ----------------------------------------------------------------------------
void TeamKartRoster::setReserveRiderItem(const std::string& item_ident)
{
    RiderItemSlot& slot = getReserveItemSlot();
    slot.m_item_ident = item_ident;
    slot.m_has_item = !item_ident.empty();
}

// ----------------------------------------------------------------------------
void TeamKartRoster::clearFrontRiderItem()
{
    m_front_item.m_item_ident.clear();
    m_front_item.m_has_item = false;
}

// ----------------------------------------------------------------------------
void TeamKartRoster::clearRearRiderItem()
{
    m_rear_item.m_item_ident.clear();
    m_rear_item.m_has_item = false;
}

// ----------------------------------------------------------------------------
void TeamKartRoster::clearActiveRiderItem()
{
    RiderItemSlot& slot = getActiveItemSlot();
    slot.m_item_ident.clear();
    slot.m_has_item = false;
}

// ----------------------------------------------------------------------------
void TeamKartRoster::clearReserveRiderItem()
{
    RiderItemSlot& slot = getReserveItemSlot();
    slot.m_item_ident.clear();
    slot.m_has_item = false;
}

// ----------------------------------------------------------------------------
bool TeamKartRoster::activeRiderHasItem() const
{
    return getActiveItemSlot().m_has_item;
}

// ----------------------------------------------------------------------------
bool TeamKartRoster::reserveRiderHasItem() const
{
    return getReserveItemSlot().m_has_item;
}

// ----------------------------------------------------------------------------
const std::string& TeamKartRoster::getFrontRiderItemIdent() const
{
    return m_front_item.m_item_ident;
}

// ----------------------------------------------------------------------------
const std::string& TeamKartRoster::getRearRiderItemIdent() const
{
    return m_rear_item.m_item_ident;
}

// ----------------------------------------------------------------------------
const std::string& TeamKartRoster::getActiveRiderItemIdent() const
{
    return getActiveItemSlot().m_item_ident;
}

// ----------------------------------------------------------------------------
const std::string& TeamKartRoster::getReserveRiderItemIdent() const
{
    return getReserveItemSlot().m_item_ident;
}

