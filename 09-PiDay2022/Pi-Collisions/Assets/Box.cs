using UnityEngine;


public class Box : MonoBehaviour
{
    public BoxManager manager;
    public long mass = 1; // in kg
    public float velocity = -1; // in m/s
    public float positionX;
    public float offset;
    float constantMultiplier;

    void Awake()
    {
        offset = transform.lossyScale.x / 2;
        positionX = transform.position.x;

        constantMultiplier = Time.fixedDeltaTime / manager.TimesPerFixedTime;
    }

    void FixedUpdate()
    {
        transform.position = new Vector3(positionX, transform.position.y, transform.position.z);
    }

    public void updatePositionX()
    {
        positionX += velocity * constantMultiplier;
    }
}
