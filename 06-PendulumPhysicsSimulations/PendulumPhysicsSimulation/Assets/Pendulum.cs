using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class Pendulum : MonoBehaviour
{
    // parameters
    public float g = 9.81f;
    public float mass = 5f;
    public float len = 1f;
    float deltatime = 0f;
   
    public float startingAngleDeg = 70f;
    public float angleDeg = 0;
    float angle = 0f;
    float angleA = 0f;
    float angleV = 0f;

    public float resistance = 0.01f;
    
    void Start()
    {
        angle = (float)(startingAngleDeg * Math.PI/180);
    }

    void FixedUpdate()
    {
        deltatime = Time.fixedDeltaTime;

        angle += angleV * deltatime;
        angleDeg = (float)(angle * 180 / Math.PI);
        angleA = getAcceleration(angle, angleV); 
        angleV += angleA * deltatime;

        transform.rotation = Quaternion.Euler(0f, 0f, angleDeg);
    }

    float getAcceleration(float angle, float angleV)
    {
        return -resistance * angleV - (float)((g / len) * Math.Sin(angle));
    }
    
}
