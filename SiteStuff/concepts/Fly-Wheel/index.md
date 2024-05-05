## Fly-Wheel

### Hardware 

The [mecanum wheel](https://en.wikipedia.org/wiki/Mecanum_wheel) is the magic behind the omni directional movement of this project.
![Mecanum Wheel Detailed diagram](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.researchgate.net%2Fprofile%2FM-Hayes-3%2Fpublication%2F311564472%2Ffigure%2Fdownload%2Ffig9%2FAS%3A525221409902601%401502233950621%2Fa-Mecanum-wheel-position-around-sphere-b-roller-angles-around-Mecanum-wheel.png&f=1&nofb=1&ipt=1327f0aa68fa2f4d1d6e701fc37b39da95684783537cc822bab735554bc7569d&ipo=images)

The mecanum wheel allows for passive diagonal movement when force is applied forwards from rotating the wheel. With a four wheel drive system and mecanum wheels allows for a combination of forwards and backwards applied forces to each wheel. This applied force turns into a diagonal force from a the passive design of the wheels. The combination of all these systems allows for an easy to manipulate net force. Being able to manipulate the robot drives net force is akin to having control of the top down 2d plain of the robots position.



### Software

Mecanum 

![Mecanum chasis diagram.](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fgm0.org%2Fen%2Flatest%2F_images%2Fmecanum-drive-force-diagram.png&f=1&nofb=1&ipt=0bcb8d050249c36d2632fc77d79e0e8490ec6b23b7f9bffb85a180fe29e6ed6d&ipo=images)

To contorl the robots movement 2 values are passed. These values are direction and magnitude. As mention in the hardware portion, the configuration and mechanical abilities of mecanum wheels allows for the manipulation of the robots movement from a top down point of view. This means with some math a combination of motor rotations can be given to acheive the desired direction and magnitude. This math just tells the wheels to rotate to acheive a desired net force.

[A short video on programing mecanum based dirve.](https://www.youtube.com/watch?v=gnSW2QpkGXQ)

