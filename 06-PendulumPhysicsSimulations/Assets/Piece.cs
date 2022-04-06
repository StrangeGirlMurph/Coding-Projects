using UnityEngine;
using System;

public class Piece : MonoBehaviour
{
    public float startingAngleDeg = 70f;


    [HideInInspector] public float angleDeg = 0;
    [HideInInspector] public double angle = 0f; // radians
    [HideInInspector] public double angleV = 0f; // m/s
    [HideInInspector] public double angleA = 0f; // m/s^2
    public double mass = 1f;
    public double length = 1f;
    double Fg; // N

    void Awake()
    {
        // angle in radians
        angle = startingAngleDeg * Math.PI / 180;

        // gravitational Force
        float g = transform.parent.gameObject.GetComponent<nPendulum>().gravitationalAcceleration;
        Fg = mass * (-g);
    }

    void FixedUpdate()
    {
        if (angle > Math.PI)
        {
            angle = -(2 * Math.PI - angle);
        }
        else if (angle < -Math.PI)
        {
            angle = (2 * Math.PI + angle);
        }

        angleDeg = (float)(angle * 180 / Math.PI);
        transform.rotation = Quaternion.Euler(0f, 0f, angleDeg);
    }

    public void UpdateAngle(float time)
    {
        angleV += angleA * time;
        angle += angleV * time;
    }
}
