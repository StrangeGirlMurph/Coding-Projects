using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMovement : MonoBehaviour
{
    public float mouseMovementSensitivity = 4f;
    public float mouseZoomingSensitivity = 1f;
    public float distance = 20f;
    public float initAngle = 20f;
    public int initHeight = 2;
    Vector3 center = Vector3.up * 5;

    // variables
    float maxAngle = 88f;
    float minAngle = 2f;
    int maxHeight = 9;
    int minHeight = 0;
    int maxDistance = 60;
    int minDistance = 0;

    
    void Start()
    {
        //Cursor.lockState = CursorLockMode.Locked;

        // - init -
        // center
        center = Vector3.up * initHeight;
        // angle
        Vector3 around = Vector3.Cross(transform.forward, Vector3.up);
        transform.RotateAround(center, around, transform.eulerAngles.x - initAngle);  
        // position
        transform.position = -transform.forward * distance + center;
    }

    
    void Update()
    {
        //Debug.DrawRay(transform.position, transform.forward * 5, Color.green, 2f);

        if (Input.GetMouseButton(0))
        {
            Vector2 turn;
            turn.x = Input.GetAxis("Mouse X") * mouseMovementSensitivity;
            turn.y = Input.GetAxis("Mouse Y") * mouseMovementSensitivity;
            transform.RotateAround(center, Vector3.up, turn.x);

            // vertical rotation
            if (transform.eulerAngles.x - turn.y >= minAngle & transform.eulerAngles.x - turn.y <= maxAngle)
            {
                Vector3 around = Vector3.Cross(transform.forward, Vector3.up);
                transform.RotateAround(center, around, turn.y);
            }
        } 

        if (Input.GetMouseButton(1))
        {
            float zoom = Input.GetAxis("Mouse X") * mouseZoomingSensitivity;
            if (distance - zoom >= minDistance & distance - zoom <= maxDistance) {
                distance -= zoom;
                transform.position = -transform.forward * distance + center;
            }
        }

        // move center
        if (Input.GetKeyDown(KeyCode.UpArrow) & center.y <= maxHeight - 1)
        {
            center += Vector3.up;
            transform.position += Vector3.up;
            transform.LookAt(center);
        }
        if (Input.GetKeyDown(KeyCode.DownArrow) & center.y >= minHeight + 1)
        {
            center += Vector3.down;
            transform.position += Vector3.down;
            transform.LookAt(center);
        }
    }
}
