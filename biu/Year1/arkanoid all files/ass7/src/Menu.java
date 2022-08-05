/**
* @author Aviv Shisman 206558157
* @param <T> the task currently "unknown" type
*/
public interface Menu<T> extends Animation {
   /**adding a selection to the menu.
    * @param key the key for selecting
    * @param message the message we get in the screen
    * @param returnVal the task to execute
    */
   void addSelection(String key, String message, T returnVal);
   /** get the current task.
    * @return returns the task
    */
   T getStatus();
}