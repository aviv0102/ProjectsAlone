
/**
* @author Aviv Shisman 206558157
* @param <T> the the unknown task
*/
public interface Task<T> {
   /** running the task.
    * @return a T value
    */
   T run();
}
