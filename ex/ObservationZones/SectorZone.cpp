/* Generated by Together */

#include "SectorZone.hpp"
#include <math.h>

GEOPOINT SectorZone::get_boundary_parametric(double t) 
{ 
  // todo: should be findlocation
  AIRCRAFT_STATE state;
  state.Location = getLocation();
  double ang = t*3.1415926*2.0;
  state.Location.Longitude += Radius*cos(ang)*0.999;
  state.Location.Latitude += Radius*sin(ang)*0.999;
  if (isInSector(state)) {
    return state.Location;
  } else {
    return getLocation();
  }
}

