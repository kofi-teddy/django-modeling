# Modeling Challenges In Django

### Short Description
How would you model players, umpires and coaches in baseball data when the same person can switch roles over the course of their life? How about servers in racks with power boards attached (and cords running across the room to remote boards)? Here is one approach to create minimal and well-performing models for such real-life situations.

### Abstract
The slightly over-simplified but useful rule of thumb when creating database schema is “normalize until it hurts, [then] denormalize until it works.” If only people didn’t skip the first step so often. 

- Modeling people who might simultaneously play different roles in the system. For example, a person who was a baseball player and then became a coach — each role has different attributes attached to it.
- Modeling what appears to be a triangular dependency relationship with minimal redundancy in the data description and without needing really long query filters to access things.
- Handling date ranges (or other measured data) of different degrees of accuracy and precision.
- working with many to many relations