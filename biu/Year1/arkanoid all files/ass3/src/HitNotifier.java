/**
* @author Aviv Shisman 206558157
*/
public interface HitNotifier {
    /** add a hit listener.
     * @param hl the hit listener*/
    void addHitListener(HitListener hl);
    /** remove a hit listener.
     * @param hl the hit listener*/
    void removeHitListener(HitListener hl);
}
