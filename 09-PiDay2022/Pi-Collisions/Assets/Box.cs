using UnityEngine;


public class Box : MonoBehaviour
{
    public BoxManager manager;
    public double mass = 1; // in kg
    public double velocity = -1; // in m/s
    public double positionX;
    public float offset;
    double constantMultiplier;

    void Awake()
    {
        offset = transform.lossyScale.x / 2;
        positionX = transform.position.x;

        constantMultiplier = Time.fixedDeltaTime / manager.repetitionsPerFrame;
    }

    void FixedUpdate()
    {
        transform.position = new Vector3((float)positionX, transform.position.y, transform.position.z);
    }

    public void updatePositionX()
    {
        positionX += velocity * constantMultiplier;
    }
}
