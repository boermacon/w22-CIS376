using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

//using Hashtable = ExitGames.Client.Photon.Hashtable;
using UnityEngine.Animations;


public class PlayerController : MonoBehaviour
{


    #region Vars
    #region Inspector Reference Vars
    [SerializeField] GameObject cameraHolder;
    [SerializeField] float mouseSenstivity, speed, jumpForce, smoothTime;
    [SerializeField] GameObject itemHolder;
    [SerializeField] GameObject weaponPivot;
    [SerializeField] GameObject Helmet, Body;
    [SerializeField] GameObject playerModel;
    [SerializeField] Camera cam;
    #endregion

    #region Location and Rotation Vars
    private float verticalLookRotation;
    bool grounded;
    Vector3 smoothMoveVelocity;
    Vector3 moveAmount;

    Vector3 moveDir, jumpDir;

    #endregion

    #region Player Vars
    Rigidbody rb;
    Hashtable customProperties = new Hashtable();
    Animator Animation;
    #endregion

    #region Health Vars
    private const float maxHealth = 45f;
    private float currentHealth = maxHealth;
    private int healthRechargeWait = 10;
    private int healthRechargePerSecond = 9;
    #endregion
    #endregion

    public float horizontalMovement;
    public float verticalMovement;
    private float distToGround;

    // Start is called before the first frame update
    void Start()
    {
        rb = gameObject.GetComponent<Rigidbody>();
        distToGround = gameObject.GetComponent<MeshCollider>().bounds.extents.y;
    }

    /// <summary>
    /// Update method called continously based on frame rate of user to handle local inputs
    /// </summary>
    private void Update()
    {

        // This will detect forward and backward movement
        horizontalMovement = Input.GetAxis("Horizontal");

        // This will detect sideways movement
        verticalMovement = Input.GetAxis("Vertical");

        //Make sure that the character only animates the idle animation while paused
        //Animation.SetFloat("InputX", 0);
        //Animation.SetFloat("InputZ", 0);

        //kill player controller if they fall into the void
        if (transform.position.y < -10f)
        {
            //Die();
        }

        //Debug.Log(Input.GetKeyDown(KeyCode.Space));
        if (Input.GetKeyDown(KeyCode.Space))
        {
            //Debug.Log(transform.up * jumpForce);
            jumpDir = transform.up * jumpForce;
        }

        moveDir = transform.forward * verticalMovement + transform.right * horizontalMovement;
    }

    /// <summary>
    /// Method is called at a fixed rate instead of being tied to framerate like update() to move the character model around the game
    /// </summary>
    private void FixedUpdate()
    {
        Look();
        if (IsGrounded())
        {
            Move();
            Jump();
        }
        //rb.velocity = moveAmount;
        //rb.MovePosition(rb.position + (transform.TransformDirection(moveAmount) * Time.fixedDeltaTime));
        //rb.velocity(Vector3.Lerp(rb.velocity)
        /*
        //Allow player to move through the air in a pause state until they are on the ground
        else if (((int)playerManager.state != 2) && !grounded)
        {
            //rb.velocity = moveAmount;
            rb.MovePosition(rb.position + (transform.TransformDirection(moveAmount) * Time.fixedDeltaTime));
        }*/
        
    }

    #region Movement
    /// <summary>
    /// Method which takes mouse inputs and converts that into camera movement in the game
    /// </summary>
    private void Look()
    {
        transform.Rotate(Vector3.up * Input.GetAxisRaw("Mouse X") * mouseSenstivity);

        //note the minus sign can be changed to a plus sign to invert mouse movement
        verticalLookRotation -= Input.GetAxisRaw("Mouse Y") * mouseSenstivity;
        verticalLookRotation = Mathf.Clamp(verticalLookRotation, -60f, 58f);

        //cameraHolder.transform.localEulerAngles = Vector3.left * verticalLookRotation;
    }

    /// <summary>
    /// Method which takes keyboard inputs and stores that into a movement amount var
    /// </summary>
    private void Move()
    {
        rb.AddForce(moveDir * speed, ForceMode.Force);

        moveDir = new Vector3(0, 0, 0);
        //rb.AddForce(Vector3.SmoothDamp(moveAmount, moveDir * speed, ref smoothMoveVelocity, smoothTime));

        //Sprint Code
        //moveAmount = Vector3.SmoothDamp(moveAmount, moveDir * (Input.GetKey(KeyCode.LeftShift) ? sprintSpeed : walkSpeed), ref smoothMoveVelocity, smoothTime);
        //moveAmount = Vector3.SmoothDamp(moveAmount, moveDir * speed, ref smoothMoveVelocity, smoothTime);

        //Tell the animator which direction the character is moving in
        //Animation.SetFloat("InputX", moveAmount.x);
        //Animation.SetFloat("InputZ", moveAmount.z);

        ///* WIP VELOCITY BASED MOVEMENT
        //Vector3 moveDir = new Vector3(Input.GetAxisRaw("Horizontal"), 0, Input.GetAxisRaw("Vertical")).normalized;
        //moveDir = transform.TransformDirection(moveDir);
        //moveAmount = moveDir ;
        //moveAmount = Vector3.SmoothDamp(moveAmount, moveDir * (Input.GetKey(KeyCode.LeftShift) ? sprintSpeed : walkSpeed), ref smoothMoveVelocity, smoothTime);
        //Tell the animator which direction the character is moving in
        //Note that this doesn't match perfectly with the movement of the character as that movement was changed from positional changes to velocity changes however there was not enough time to find a solution
        //Animation.SetFloat("InputX", Input.GetAxisRaw("Horizontal") * (Input.GetKey(KeyCode.LeftShift) ? sprintSpeed : walkSpeed) * smoothTime);
        //Animation.SetFloat("InputZ", Input.GetAxisRaw("Vertical") * (Input.GetKey(KeyCode.LeftShift) ? sprintSpeed : walkSpeed) * smoothTime);
        //*/
    }

    /// <summary>
    /// Method which allows character to jump if they are on the ground
    /// </summary>
    private void Jump()
    {
        //Debug.Log(jumpDir);
        rb.AddForce(jumpDir, ForceMode.Force);
        jumpDir = new Vector3(0, 0, 0);
    }

    private bool IsGrounded() {
        //Debug.Log(Physics.Raycast(transform.position, -Vector3.up, distToGround + 0.2f));
        return Physics.Raycast(transform.position, -Vector3.up, distToGround + 0.2f);
    }

private void OnCollisionEnter(Collision collision)
    {
        if(collision.gameObject.tag == "Terrain")
        {
            grounded = true;
        }
    }
    private void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.tag == "Terrain")
        {
            grounded = false;
        }
    }
    #endregion
}